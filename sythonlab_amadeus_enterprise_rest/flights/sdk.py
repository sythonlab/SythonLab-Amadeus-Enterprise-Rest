#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: sdk.py
Author: Sython Lab (sythonlab@gmail.com)
Created: 2025-12-04
"""

import logging
from datetime import datetime, timezone
from typing import List, Any, Optional
from uuid import uuid4

import requests

from sythonlab_amadeus_enterprise_rest import settings
from sythonlab_amadeus_enterprise_rest.core.enums import Currency, TravelerType, PaymentMethod, RequestMethod, \
    CommissionType, CardBrand
from sythonlab_amadeus_enterprise_rest.flights.dataclasses import SearchAvailabilityItinerary, SearchAvailabilityPax, \
    ReservePax, PaymentData
from sythonlab_amadeus_enterprise_rest.flights.endpoints import FlightEndpoints

logger = logging.getLogger(__name__)


class FlightSDK:
    """SDK for interacting with Amadeus Enterprise REST Flight APIs."""

    ama_ref = None
    prefix_ama_ref = ""
    suffix_ama_ref = ""
    currency = Currency.USD
    auth_data = None
    debug = False

    def __init__(self, *, prefix_ama_ref: str = "", suffix_ama_ref: str = "", currency: Currency = Currency.USD,
                 debug: bool = False, ama_ref: str = None):
        """Initialize the FlightSDK with optional parameters."""

        self.currency = currency
        self.debug = debug
        self.prefix_ama_ref = prefix_ama_ref
        self.suffix_ama_ref = suffix_ama_ref

    def build_ama_ref(self):
        """Generate a unique ama-client-ref for tracking requests."""

        now = datetime.now(timezone.utc)
        iso = now.isoformat(timespec="milliseconds").replace("+00:00", "Z")

        return f"{self.prefix_ama_ref}/{iso}/{str(uuid4())}/{self.suffix_ama_ref}"

    @property
    def access_token(self):
        """Retrieve the access token from auth_data if available."""

        if self.auth_data:
            return self.auth_data.get("access_token")
        return None

    def build_headers(self, headers: Optional[Any] = None, use_json: bool = True, no_auth: bool = False):
        """Build request headers, adding Content-Type and Authorization if not provided."""

        if not headers:
            headers = {}

        if not headers.get("Content-Type"):
            headers["Content-Type"] = "application/json" if use_json else "application/x-www-form-urlencoded"

        if not no_auth and not headers.get("Authorization") and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        headers["ama-client-ref"] = self.build_ama_ref()

        return headers

    def request(self, *, url: str, payload: Any = None, headers: Optional[dict] = None, use_json: bool = True,
                method: RequestMethod = RequestMethod.POST, no_auth: bool = False, show_response: bool = False):
        """Make an HTTP request to the specified URL with the given payload and headers."""

        headers = self.build_headers(headers, use_json=use_json, no_auth=no_auth)

        if not payload:
            payload = {}

        start = datetime.now(timezone.utc)

        if self.debug:
            logger.debug("-" * 100)
            logger.debug("URL: %s", url)
            logger.debug("Start time: %s", start.strftime("%d/%m/%Y %H:%M:%S"))
            logger.debug("Headers: %s", headers)
            logger.debug("Payload: %s", payload)

        if method == RequestMethod.POST:
            if use_json:
                response = requests.post(url, json=payload, headers=headers)
            else:
                response = requests.post(url, data=payload, headers=headers)
        elif method == RequestMethod.PATCH:
            response = requests.patch(url, json=payload, headers=headers)
        elif method == RequestMethod.GET:
            response = requests.get(url, params=payload, headers=headers)
        elif method == RequestMethod.DELETE:
            response = requests.delete(url, params=payload, headers=headers)
        else:
            raise ValueError("Unsupported request method")

        if self.debug:
            end = datetime.now(timezone.utc)

            logger.debug("-" * 100)
            logger.debug("End time: %s", end.strftime("%d/%m/%Y %H:%M:%S"))
            logger.debug("Duration: %s", end - start)
            logger.debug("Response status: %s", response.status_code)

            if show_response:
                try:
                    logger.debug("Response data: %s", response.json())
                except Exception:
                    logger.debug("Response raw data: %s", response.text)

        if method == RequestMethod.DELETE and response.status_code == 204:
            return response.status_code, {}

        return response.status_code, response.json()

    def login(self):
        """Authenticate and obtain an access token."""

        payload = {
            "grant_type": "client_credentials",
            "client_id": settings.AMADEUS_CONFIG.get("CLIENT_ID"),
            "client_secret": settings.AMADEUS_CONFIG.get("CLIENT_SECRET"),
        }

        status, data = self.request(url=FlightEndpoints.FLIGHT_LOGIN_ENDPOINT.value, payload=payload, use_json=False,
                                    no_auth=True)

        if status == 200:
            self.auth_data = data

    def search_availability(self, *, itinerary: List[SearchAvailabilityItinerary],
                            travelers: List[SearchAvailabilityPax], only_carriers: Optional[List[str]] = None):
        """Search for flight availability based on the provided itinerary and travelers."""

        self.login()

        filters = {}

        if only_carriers:
            filters = {
                "flightFilters": {
                    "carrierRestrictions": {
                        "includedCarrierCodes": only_carriers
                    }
                }
            }

        payload = {
            "currencyCode": self.currency.value,
            "originDestinations": [
                {
                    "id": route.id,
                    "originLocationCode": route.origin_location_code,
                    "destinationLocationCode": route.destination_location_code,
                    "departureDateTimeRange": {
                        "date": route.departure_date
                    }
                }
                for route in itinerary
            ],
            "travelers": [
                {
                    "id": pax.id,
                    "travelerType": pax.traveler_type.value,
                    "fareOptions": [
                        "STANDARD"
                    ],
                    **({"associatedAdultId": "1"} if pax.traveler_type == TravelerType.INFANT else {})
                }
                for pax in travelers
            ],
            "sources": [
                "GDS"
            ],
            "searchCriteria": {
                "pricingOptions": {
                    "fareType": [
                        "PUBLISHED"
                    ]
                },
                "additionalInformation": {
                    "brandedFares": True
                },
                **filters
            }
        }

        return self.request(url=FlightEndpoints.FLIGHT_AVAILABILITY_ENDPOINT.value, payload=payload)

    def pricing(self, *, flight_data: Any, payment_method: PaymentMethod, card_brand: Optional[CardBrand] = None):
        """Payload should be the flight offers obtained from search_availability method."""

        self.login()

        extra = {}

        if payment_method == PaymentMethod.CREDIT_CARD:
            extra.update({
                "payments": [{
                    "brand": card_brand.value,
                    "flightOfferIds": [flight_data.get("id")]
                }]
            })

        payload = {
            "data": {
                "type": "flight-offers-pricing",
                "flightOffers": [
                    flight_data
                ],
                **extra
            }
        }

        return self.request(url=FlightEndpoints.FLIGHT_PRICING_ENDPOINT.value, payload=payload)

    def retrieve_by_locator(self, *, locator: str):
        """Retrieve a reservation by its locator code."""

        self.login()

        return self.request(
            url=f"{FlightEndpoints.FLIGHT_RETRIEVE_BOOKING_BY_LOCATOR_ENDPOINT.value}&reference={locator}",
            method=RequestMethod.GET,
            show_response=True
        )

    def retrieve_by_booking_id(self, *, booking_id: str):
        """Retrieve a reservation by its booking ID."""

        self.login()

        return self.request(
            url=f"{FlightEndpoints.FLIGHT_RETRIEVE_BOOKING_BY_ID_ENDPOINT.value}/{booking_id}",
            method=RequestMethod.GET,
            show_response=True
        )

    def issue_booking(self, *, booking_id: str):
        """Issue a reservation by its booking ID."""

        self.login()

        return self.request(
            url=f"{FlightEndpoints.FLIGHT_ISSUE_BOOKING_ENDPOINT.value}/{booking_id}/issuance",
            show_response=True
        )

    def cancel_booking(self, *, booking_id: str):
        """Cancel a reservation by its booking ID."""

        self.login()

        return self.request(
            url=f"{FlightEndpoints.FLIGHT_CANCEL_BOOKING_ENDPOINT.value}/{booking_id}",
            method=RequestMethod.DELETE
        )

    def fm_commission_booking(self, *, booking_id: str, commission_type: CommissionType, value: float):
        """Add a commission to a reservation by its booking ID."""

        self.login()

        return self.request(
            url=f"{FlightEndpoints.FLIGHT_FM_COMMISSION_BOOKING_ENDPOINT.value}/{booking_id}",
            method=RequestMethod.PATCH,
            payload={
                "data": {
                    "type": "flight-order",
                    "commissions": [
                        {
                            "controls": [
                                "MANUAL"
                            ],
                            "values": [
                                {
                                    "commissionType": "NEW",
                                    **{commission_type.value: value}
                                }
                            ]
                        }
                    ]
                }
            }
        )

    def reserve(self, *, pricing_data: Any, payment_method: PaymentMethod, travelers: List[ReservePax],
                payment_data: Optional[PaymentData] = None):
        """Reserve a flight based on the provided pricing data, payment method, and traveler information."""

        self.login()

        payments = []

        match payment_method:
            case PaymentMethod.CASH:
                payments = [{
                    "other": {
                        "method": "CASH",
                        "flightOfferIds": [
                            pricing_data.get("id")
                        ]
                    }
                }]
            case PaymentMethod.CREDIT_CARD:
                payments = [{
                    "creditCard": {
                        "brand": payment_data.brand.value,
                        "holder": payment_data.holder,
                        "number": payment_data.number,
                        "expiryDate": payment_data.expiry_date,
                        "securityCode": payment_data.security_code,
                        "flightOfferIds": [
                            pricing_data.get("id")
                        ]
                    }
                }]

        payload = {
            "data": {
                "type": "flight-order",
                "flightOffers": [
                    pricing_data
                ],
                "travelers": [
                    {
                        "id": traveler.id,
                        "dateOfBirth": traveler.date_of_birth,
                        "name": {
                            "firstName": traveler.first_name,
                            "lastName": traveler.last_name
                        },
                        "gender": traveler.gender.value,
                        "contact": {
                            "emailAddress": traveler.email,
                            "phones": [
                                {
                                    "deviceType": "MOBILE",
                                    "countryCallingCode": traveler.phone_country_code,
                                    "number": traveler.phone_number
                                }
                            ]
                        },
                        "documents": [
                            {
                                "documentType": traveler.document_type.value,
                                "number": traveler.document_number,
                                "issuanceDate": traveler.document_issuance_date,
                                "expiryDate": traveler.document_expiry_date,
                                "issuanceCountry": traveler.document_issuance_country_code,
                                "nationality": traveler.nationality_code,
                                "holder": True
                            }
                        ]
                    } for traveler in travelers
                ],
                "formOfPayments": [
                    *payments
                ]
            }
        }

        return self.request(url=FlightEndpoints.FLIGHT_RESERVE_ENDPOINT.value, payload=payload, show_response=True)
