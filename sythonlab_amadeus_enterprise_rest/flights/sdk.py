from typing import List, Any, Optional

import requests

from sythonlab_amadeus_enterprise_rest import settings
from sythonlab_amadeus_enterprise_rest.core.enums import Currency, TravelerType
from sythonlab_amadeus_enterprise_rest.flights.dataclasses import SearchAvailabilityItinerary, SearchAvailabilityPax
from sythonlab_amadeus_enterprise_rest.flights.endpoints import FlightEndpoints


class FlightSDK:
    currency = "USD"
    auth_data = None
    debug = False

    def __init__(self, *, currency: Currency = Currency.JMD, debug: bool = False):
        self.currency = currency
        self.debug = debug

    @property
    def access_token(self):
        if self.auth_data:
            return self.auth_data.get('access_token')
        return None

    def build_headers(self, headers: Optional[Any] = None, use_json: bool = True):
        if not headers:
            headers = {}

        if not headers.get('Content-Type'):
            headers['Content-Type'] = 'application/json' if use_json else 'application/x-www-form-urlencoded'

        if not headers.get('Authorization') and self.access_token:
            headers['Authorization'] = f"Bearer {self.access_token}"

        return headers

    def request(self, *, url: str, payload: Any, headers: Optional[dict] = None, use_json: bool = True):
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

        status, data = self.request(url=FlightEndpoints.FLIGHT_AVAILABILITY_ENDPOINT.value, payload=payload)
