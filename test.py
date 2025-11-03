from sythonlab_amadeus_enterprise_rest.core.enums import TravelerType, Currency
from sythonlab_amadeus_enterprise_rest.flights.dataclasses import SearchAvailabilityItinerary, SearchAvailabilityPax
from sythonlab_amadeus_enterprise_rest.flights.sdk import FlightSDK

sdk = FlightSDK(debug=True, prefix_ama_ref="CLT", suffix_ama_ref="user1", currency=Currency.JMD)

availability_status, availability_data = sdk.search_availability(itinerary=[
    SearchAvailabilityItinerary(id="1", originLocationCode="CDG", destinationLocationCode="FRA",
                                departureDateTimeRange="2025-11-16"),
    SearchAvailabilityItinerary(id="2", originLocationCode="FRA", destinationLocationCode="CDG",
                                departureDateTimeRange="2025-11-23")
], travelers=[
    SearchAvailabilityPax(id="1", travelerType=TravelerType.ADULT),
    SearchAvailabilityPax(id="2", travelerType=TravelerType.CHILD),
    SearchAvailabilityPax(id="3", travelerType=TravelerType.INFANT),
])

if availability_status == 200:
    pricing_status, pricing_data = sdk.pricing(flight_data=availability_data["data"][0])
