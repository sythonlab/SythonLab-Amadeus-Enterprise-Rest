from sythonlab_amadeus_enterprise_rest.core.enums import TravelerType
from sythonlab_amadeus_enterprise_rest.flights.dataclasses import SearchAvailabilityItinerary, SearchAvailabilityPax
from sythonlab_amadeus_enterprise_rest.flights.sdk import FlightSDK

sdk = FlightSDK(debug=True)

sdk.search_availability(itinerary=[
    SearchAvailabilityItinerary(id="1", originLocationCode="CDG", destinationLocationCode="FRA",
                                departureDateTimeRange="2025-11-16"),
    SearchAvailabilityItinerary(id="2", originLocationCode="FRA", destinationLocationCode="CDG",
                                departureDateTimeRange="2025-11-23")
], travelers=[
    SearchAvailabilityPax(id="1", travelerType=TravelerType.ADULT),
    SearchAvailabilityPax(id="2", travelerType=TravelerType.CHILD),
    SearchAvailabilityPax(id="3", travelerType=TravelerType.INFANT),
])
