from sythonlab_amadeus_enterprise_rest.core.enums import TravelerType, Currency
from sythonlab_amadeus_enterprise_rest.flights.dataclasses import SearchAvailabilityItinerary, SearchAvailabilityPax
from sythonlab_amadeus_enterprise_rest.flights.sdk import FlightSDK

sdk = FlightSDK(debug=True, prefix_ama_ref="CLT", suffix_ama_ref="user1", currency=Currency.JMD)

availability_status, availability_data = sdk.search_availabilities(itinerary=[
    SearchAvailabilityItinerary(
        id="1",
        origin_location_code="KIN",
        destination_location_code="MIA",
        departure_date="2026-05-15"
    ),
    SearchAvailabilityItinerary(
        id="2",
        origin_location_code="MIA",
        destination_location_code="KIN",
        departure_date="2026-05-27"
    )
], travelers=[
    SearchAvailabilityPax(id="1", traveler_type=TravelerType.ADULT),
    SearchAvailabilityPax(id="2", traveler_type=TravelerType.ADULT),
    SearchAvailabilityPax(id="3", traveler_type=TravelerType.CHILD),
    SearchAvailabilityPax(id="4", traveler_type=TravelerType.INFANT),
])
