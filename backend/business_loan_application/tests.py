from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import LoanApplicationTransaction
from .constants import INITIATED_STEP, RETRIEVED_BALANCE_SHEET_STEP, DECISION_RESULT_SENT_TO_USER_STEP

'''
NOTE: In practice, it's not a good idea to test business logic by testing APIs especially if testing said API triggers an API call to an external system.
Better to refactor the business logic to a core function and test that core function directly.
Moreover, for those core functions that triggers an API call to an external system,
we can implement a mock of the API call so that an actual API call is not made and can still be tested.
Testing API calls is best done for testing the authentication and authorization of the APIs and even if that's the case,
its better to test the interface rather than the actual API
i.e. create a mock API with reusable authentications and authorizations mixins which is then reused in other parts of the system.
'''



class ApiTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = APIClient()
        self.client.login(username='test', password='test')

    def test_main_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()
        response = self.client.get('')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_initiate_application_api(self):
        response = self.client.post('/initiate-application/', {}, format='json')
        response_data = response.json()
        transaction_id = response_data.get('data', {}).get('transaction_id')
        queryset = LoanApplicationTransaction.objects.all()
        self.assertEqual(len(queryset), 1)
        
        transaction = queryset[0]
        self.assertEqual(transaction.steps, INITIATED_STEP)
        return transaction.id

    def test_save_loan_application_detail_api(self):
        transaction_id = self.test_initiate_application_api()
        request_data = {
            'transaction_id': transaction_id,
            'name': 'foo',
            'year_established': '2020',
            'summary_of_profit_or_loss': '10000',
            'loan_amount': '10000',
            'accounting_software_key': 'MYOB',
        }

        response = self.client.post('/save-loan-application-details/', request_data, format='json')

        transaction = LoanApplicationTransaction.objects.get(id=transaction_id)
        application_details = transaction.get_application_details()
        self.assertEqual(request_data['name'], application_details['name'])
        self.assertEqual(request_data['year_established'], application_details['year_established'])
        self.assertEqual(float(request_data['summary_of_profit_or_loss']), application_details['summary_of_profit_or_loss'])
        self.assertEqual(float(request_data['loan_amount']), application_details['loan_amount'])
        self.assertEqual(request_data['accounting_software_key'], application_details['accounting_software_key'])
        return transaction.id

    def test_invalid_save_loan_application_details_api(self):
        transaction_id = self.test_initiate_application_api()
        INVALID_SOFTWARE_KEY = 'FOO'
        response = self.client.post('/save-loan-application-details/', {
            'transaction_id': transaction_id,
            'name': 'foo',
            'year_established': '2020',
            'summary_of_profit_or_loss': '10000',
            'loan_amount': '10000',
            'accounting_software_key': INVALID_SOFTWARE_KEY,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data.get('success'), False)
        self.assertIn(response_data.get('message'), f'accounting_software_key: "{INVALID_SOFTWARE_KEY}" is not a valid choice.')
    
    def test_request_balance_sheet_api(self):
        transaction_id = self.test_save_loan_application_detail_api()
        response = self.client.post('/request-balance-sheet/', {"transaction_id": transaction_id}, format='json')
        response_data = response.json()
        
        self.assertTrue(response_data.get('data', {}).get('balance_sheet', []))

        transaction = LoanApplicationTransaction.objects.get(id=transaction_id)
        self.assertEqual(transaction.steps, RETRIEVED_BALANCE_SHEET_STEP)

        balance_sheet = transaction.get_balance_sheet()
        self.assertTrue(balance_sheet)
        return transaction_id

    def test_invalid_request_balance_sheet_api(self):
        # Purposely change the step to be an invalid step for this operation
        transaction_id = self.test_save_loan_application_detail_api()
        transaction = LoanApplicationTransaction.objects.get(id=transaction_id)
        transaction.steps = RETRIEVED_BALANCE_SHEET_STEP
        transaction.save(update_fields=['steps'])

        response = self.client.post('/request-balance-sheet/', {"transaction_id": transaction_id}, format='json')
        response_data = response.json()
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Unable to execute this functionality with the current loan application step.')

    def test_submit_application_api(self):
        transaction_id = self.test_request_balance_sheet_api()
        transaction = LoanApplicationTransaction.objects.get(id=transaction_id)
        response = self.client.post('/submit-application/', {"transaction_id": transaction_id}, format='json')
        response_data = response.json()
        decision_outcome = response_data.get('data', {}).get('decision_outcome', "")
        self.assertEqual(decision_outcome, transaction.get_decision_outcome())
        self.assertEqual(transaction.steps, DECISION_RESULT_SENT_TO_USER_STEP)
        self.assertTrue(transaction.get_pre_assessment_value())
        self.assertTrue(transaction.get_decision_outcome())

    def test_invalid_submit_application_api(self):
        # Purposely change the step to be an invalid step for this operation
        transaction_id = self.test_request_balance_sheet_api()
        transaction = LoanApplicationTransaction.objects.get(id=transaction_id)
        transaction.steps = INITIATED_STEP
        transaction.save(update_fields=['steps'])

        response = self.client.post('/submit-application/', {"transaction_id": transaction_id}, format='json')
        response_data = response.json()
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Unable to execute this functionality with the current loan application step.')
