from enum import Enum

from sythonlab_amadeus_enterprise_rest import settings

FLIGHT_URL_BASE = settings.AMADEUS_CONFIG.get('API_URL')


class FlightEndpoints(Enum):
    FLIGHT_LOGIN_ENDPOINT = f"{FLIGHT_URL_BASE}/v1/security/oauth2/token"
    FLIGHT_AVAILABILITY_ENDPOINT = f"{FLIGHT_URL_BASE}/v2/shopping/flight-offers"
    FLIGHT_PRICING_ENDPOINT = f"{FLIGHT_URL_BASE}/v1/shopping/flight-offers/pricing"
    FLIGHT_RESERVE_ENDPOINT = f"{FLIGHT_URL_BASE}/v1/booking/flight-orders"
