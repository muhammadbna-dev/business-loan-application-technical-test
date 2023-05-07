import logging

from .base import BaseAdapter
from .utils.serializer_utils import serialize_balance_sheet_data

STUB_RESPONSE = [
    {
        "year": 2020,
        "month": 12,
        "profitOrLoss": 250000,
        "assetsValue": 1234
    },
    {
        "year": 2020,
        "month": 11,
        "profitOrLoss": 1150,
        "assetsValue": 5789
    },
    {
        "year": 2020,
        "month": 10,
        "profitOrLoss": 2500,
        "assetsValue": 22345
    },
    {
        "year": 2020,
        "month": 9,
        "profitOrLoss": -187000,
        "assetsValue": 223452
    }
]

class MyobAdapter(BaseAdapter):

    def _get_credentials(self):
        # NOTE: Credentials should be stored in the team level that the Applicant is in
        # This is implemented this way because managing credentials for different accounting softwares is not within the scope of the proect
        return "dummy_credentials_myob"

    def _get_and_transform_data_for_request(self):
        application_details = self.loan_application_transaction.get_application_details()
        return {
            'myob_name': application_details.get("name", ""),
            'myob_year_established': application_details.get("year_established", ""),
            'myob_summary_of_profit_or_loss': application_details.get("summary_of_profit_or_loss", ""),
            'myob_loan_amount': application_details.get("loan_amount", ""),
        }

    def _call_api(self, credentials, request_data):
        return STUB_RESPONSE

    def _transform_data_from_response(self, response_data):
        serialized_data = []
        for data in response_data:
            obj = serialize_balance_sheet_data(
                data['year'],
                data['month'],
                data['profitOrLoss'],
                data['assetsValue'],
            )
            serialized_data.append(obj)
        return serialized_data

    def request_balance_sheet(self):
        try:
            credentials = self._get_credentials()
            request_data = self._get_and_transform_data_for_request()
            response_data = self._call_api(credentials, request_data)
            data = self._transform_data_from_response(response_data)
            return data, True
        except Exception as inst:
            logging.exception(f"Error retrieving balance sheet data for transaction ID ${self.loan_application_transaction.id}. Exception details: ${inst}")
            return [], False
