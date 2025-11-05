from sythonlab_amadeus_enterprise_rest.core.enums import Currency
from sythonlab_amadeus_enterprise_rest.flights.sdk import FlightSDK

sdk = FlightSDK(debug=True, prefix_ama_ref="CLT", suffix_ama_ref="user1", currency=Currency.JMD)

retrieve_by_id_status, retrieve_by_id_data = sdk.retrieve_by_booking_id(booking_id="eJzTd9d39PYzCwoBAAsAAlw")
