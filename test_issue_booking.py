from sythonlab_amadeus_enterprise_rest.core.enums import Currency, CommissionType
from sythonlab_amadeus_enterprise_rest.flights.sdk import FlightSDK

LOCATOR = "BTFD67"

sdk = FlightSDK(debug=True, prefix_ama_ref="CLT", suffix_ama_ref="user1", currency=Currency.JMD)

retrieve_status, retrieve_data = sdk.retrieve_by_locator(locator=LOCATOR)

if retrieve_status == 200:
    commission_status, commission_data = sdk.fm_commission_booking(booking_id=retrieve_data.get('data')[0].get('id'),
                                                                   commission_type=CommissionType.PERCENTAGE, value=2)

    if commission_status == 200:
        issue_status, issue_data = sdk.issue_booking(booking_id=retrieve_data.get('data')[0].get('id'))
