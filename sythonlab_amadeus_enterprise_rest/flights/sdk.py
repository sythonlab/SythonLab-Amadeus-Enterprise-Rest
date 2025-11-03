from datetime import datetime
from typing import List, Any, Optional
from uuid import uuid4

import requests

from sythonlab_amadeus_enterprise_rest import settings
from sythonlab_amadeus_enterprise_rest.core.enums import Currency, TravelerType
from sythonlab_amadeus_enterprise_rest.flights.dataclasses import SearchAvailabilityItinerary, SearchAvailabilityPax
from sythonlab_amadeus_enterprise_rest.flights.endpoints import FlightEndpoints


class FlightSDK:
    ama_ref = None
    prefix_ama_ref = ""
    suffix_ama_ref = ""
    currency = Currency.USD
    auth_data = None
    debug = False

    def __init__(self, *, prefix_ama_ref: str = "", suffix_ama_ref: str = "", currency: Currency = Currency.USD,
                 debug: bool = False, ama_ref: str = None):
        self.currency = currency
        self.debug = debug
        self.prefix_ama_ref = prefix_ama_ref
        self.suffix_ama_ref = suffix_ama_ref
        if not ama_ref:
            self.ama_ref = self.build_ama_ref()
        else:
            self.ama_ref = ama_ref

    def build_ama_ref(self):
        return f"{self.prefix_ama_ref}/{datetime.now().timestamp()}/{str(uuid4())}/{self.suffix_ama_ref}"

    @property
    def access_token(self):
        """Retrieve the access token from auth_data if available."""

        if self.auth_data:
            return self.auth_data.get('access_token')
        return None

    def build_headers(self, headers: Optional[Any] = None, use_json: bool = True):
        """Build request headers, adding Content-Type and Authorization if not provided."""

        if not headers:
            headers = {}

        if not headers.get('Content-Type'):
            headers['Content-Type'] = 'application/json' if use_json else 'application/x-www-form-urlencoded'

        if not headers.get('Authorization') and self.access_token:
            headers['Authorization'] = f"Bearer {self.access_token}"

        if self.ama_ref:
            headers['ama-client-ref'] = self.ama_ref

        return headers

    def request(self, *, url: str, payload: Any, headers: Optional[dict] = None, use_json: bool = True):
        """Make a POST request to the specified URL with the given payload and headers."""

        headers = self.build_headers(headers, use_json=use_json)

        if self.debug:
            print('-' * 100)
            print("URL:", url)
            print('Headers:', headers)
            print("Payload:", payload)

        if use_json:
            response = requests.post(url, json=payload, headers=headers)
        else:
            response = requests.post(url, data=payload, headers=headers)

        if self.debug:
            print("Response status:", response.status_code)
            try:
                print("Response data:", response.json())
            except Exception:
                print("Response raw data:", response.text)

        return response.status_code, response.json()

    def login(self):
        """Authenticate and obtain an access token."""

        payload = {
            "grant_type": "client_credentials",
            "client_id": settings.AMADEUS_CONFIG.get('CLIENT_ID'),
            "client_secret": settings.AMADEUS_CONFIG.get('CLIENT_SECRET'),
        }

        status, data = self.request(url=FlightEndpoints.FLIGHT_LOGIN_ENDPOINT.value, payload=payload, use_json=False)

        if status == 200:
            self.auth_data = data

    def search_availability(self, *, itinerary: List[SearchAvailabilityItinerary],
                            travelers: List[SearchAvailabilityPax]):
        """Search for flight availability based on the provided itinerary and travelers."""

        self.login()

        payload = {
            "currencyCode": self.currency.value,
            "originDestinations": [
                {
                    "id": route.id,
                    "originLocationCode": route.originLocationCode,
                    "destinationLocationCode": route.destinationLocationCode,
                    "departureDateTimeRange": {
                        "date": route.departureDateTimeRange
                    }
                }
                for route in itinerary
            ],
            "travelers": [
                {
                    "id": pax.id,
                    "travelerType": pax.travelerType.value,
                    "fareOptions": [
                        "STANDARD"
                    ],
                    **({"associatedAdultId": "1"} if pax.travelerType == TravelerType.INFANT else {})
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
                }
            }
        }

        return self.request(url=FlightEndpoints.FLIGHT_AVAILABILITY_ENDPOINT.value, payload=payload)

    def pricing(self, *, flight_data: Any):
        """Payload should be the flight offers obtained from search_availability method."""

        self.login()

        payload = {
            "data": {
                "type": "flight-offers-pricing",
                "flightOffers": [
                    flight_data
                ]
            }
        }

        return self.request(url=FlightEndpoints.FLIGHT_PRICING_ENDPOINT.value, payload=payload)
