from sythonlab_amadeus_enterprise_rest.core.enums import Currency
from sythonlab_amadeus_enterprise_rest.flights.sdk import FlightSDK

sdk1 = FlightSDK(debug=True, prefix_ama_ref="Test", suffix_ama_ref="user1", currency=Currency.JMD)

sdk1.login()

sdk2 = FlightSDK(
    debug=True, prefix_ama_ref="Test", suffix_ama_ref="user1", currency=Currency.JMD, access_token=sdk1.access_token
)

sdk2.login()
