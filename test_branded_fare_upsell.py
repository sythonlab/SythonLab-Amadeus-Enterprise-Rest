from sythonlab_amadeus_enterprise_rest.core.enums import TravelerType, Currency, PaymentMethod, Gender, DocumentType
from sythonlab_amadeus_enterprise_rest.flights.dataclasses import SearchAvailabilityItinerary, SearchAvailabilityPax, \
    ReservePax
from sythonlab_amadeus_enterprise_rest.flights.sdk import FlightSDK

sdk = FlightSDK(debug=True, prefix_ama_ref="CLT", suffix_ama_ref="user1", currency=Currency.JMD)

availability_status, availability_data = sdk.search_availability(itinerary=[
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
])

if availability_status == 200:
    if availability_data.get("data", []):
        pricing_status, pricing_data = sdk.pricing(flight_data=availability_data["data"][0],
                                                   payment_method=PaymentMethod.CASH)

        if pricing_status == 200:
            if pricing_data.get("data", {}).get("flightOffers", []):
                upsell_status, upsell_data = sdk.branded_fare_upsell(
                    pricing_data=pricing_data["data"]["flightOffers"][0],
                )
            else:
                print("No flight offers found in pricing data.")
    else:
        print("No flights found")
