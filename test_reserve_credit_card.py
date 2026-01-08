from sythonlab_amadeus_enterprise_rest.core.enums import TravelerType, Currency, PaymentMethod, Gender, DocumentType, \
    CardBrand
from sythonlab_amadeus_enterprise_rest.flights.dataclasses import SearchAvailabilityItinerary, SearchAvailabilityPax, \
    ReservePax, PaymentData
from sythonlab_amadeus_enterprise_rest.flights.sdk import FlightSDK

sdk = FlightSDK(debug=True, prefix_ama_ref="CLT", suffix_ama_ref="user1", currency=Currency.JMD)

availability_status, availability_data = sdk.search_availability(itinerary=[
    SearchAvailabilityItinerary(id="1", origin_location_code="BOG", destination_location_code="MIA",
                                departure_date="2026-02-10"),
    SearchAvailabilityItinerary(id="2", origin_location_code="MIA", destination_location_code="BOG",
                                departure_date="2026-02-20")
], travelers=[
    SearchAvailabilityPax(id="1", traveler_type=TravelerType.ADULT),
    # SearchAvailabilityPax(id="2", traveler_type=TravelerType.CHILD),
    # SearchAvailabilityPax(id="3", traveler_type=TravelerType.INFANT),
], only_carriers=["CM"])

if availability_status == 200:
    pricing_status, pricing_data = sdk.pricing(
        flight_data=availability_data["data"][0], payment_method=PaymentMethod.CREDIT_CARD,
        card_brand=CardBrand.AMERICAN_EXPRESS
    )

    if pricing_status == 200:
        reserve_status, reserve_data = sdk.reserve(
            pricing_data=pricing_data["data"]["flightOffers"][0],
            payment_method=PaymentMethod.CREDIT_CARD,
            payment_data=PaymentData(
                brand=CardBrand.AMERICAN_EXPRESS,
                holder="CORPORATE",
                number="370000000000002",
                expiry_date="2030-03",
                security_code="1234",
            ),
            travelers=[
                ReservePax(id="1", date_of_birth="1992-12-28", first_name="Jose Angel", last_name="Alvarez Abraira",
                           gender=Gender.MALE, email="jaalvarez2818@gmail.com", phone_country_code="34",
                           phone_number="697676672", document_type=DocumentType.PASSPORT, document_number="K111111",
                           document_issuance_date="2024-05-01", document_expiry_date="2026-05-01",
                           document_issuance_country_code="CU", nationality_code="CU"),
                # ReservePax(id="2", date_of_birth="2019-05-18", first_name="Chabelly", last_name="Motes Penna",
                #            gender=Gender.FEMALE, email="chabellyprueba123@gmail.com", phone_country_code="53",
                #            phone_number="55555554", document_type=DocumentType.PASSPORT, document_number="K222222",
                #            document_issuance_date="2024-06-01", document_expiry_date="2026-06-01",
                #            document_issuance_country_code="ES", nationality_code="ES"),
                # ReservePax(id="3", date_of_birth="2024-04-22", first_name="Eleany", last_name="Gutierrez Morrell",
                #            gender=Gender.FEMALE, email="eleanyprueba123@gmail.com", phone_country_code="53",
                #            phone_number="55555555", document_type=DocumentType.PASSPORT, document_number="K333333",
                #            document_issuance_date="2024-07-01", document_expiry_date="2026-07-01",
                #            document_issuance_country_code="US", nationality_code="US"),
            ]
        )
