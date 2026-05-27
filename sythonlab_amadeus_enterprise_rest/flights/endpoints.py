#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: endpoints.py
Author: Sython Lab (sythonlab@gmail.com)
Created: 2025-12-04
"""

from enum import Enum


class FlightEndpoints(Enum):
    """Endpoints for Amadeus Flight API."""

    FLIGHT_LOGIN_ENDPOINT = "/v1/security/oauth2/token"
    FLIGHT_AVAILABILITY_ENDPOINT = "/v2/shopping/flight-offers"
    FLIGHT_AVAILABILITIES_ENDPOINT = "/v1/shopping/availability/flight-availabilities"
    FLIGHT_PRICING_ENDPOINT = "/v1/shopping/flight-offers/pricing"
    FLIGHT_RESERVE_ENDPOINT = "/v1/booking/flight-orders"
    FLIGHT_RETRIEVE_BOOKING_BY_LOCATOR_ENDPOINT = "/v1/booking/flight-orders/by-reference?originSystemCode=GDS"
    FLIGHT_RETRIEVE_BOOKING_BY_ID_ENDPOINT = f"/v1/booking/flight-orders"
    FLIGHT_CANCEL_BOOKING_ENDPOINT = "/v1/booking/flight-orders"
    FLIGHT_ISSUE_BOOKING_ENDPOINT = "/v1/booking/flight-orders"
    FLIGHT_FM_COMMISSION_BOOKING_ENDPOINT = "/v1/booking/flight-orders"
    FLIGHT_BRANDED_FARE_UPSELL = "/v1/shopping/flight-offers/upselling"
    FLIGHT_QUEUE_LIST = "/v1/office/queues"


def get_flight_endpoint(api_url: str, endpoint: FlightEndpoints):
    return f"{api_url}{endpoint.value}"
