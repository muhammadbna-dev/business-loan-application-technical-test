import logging
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import LoanApplicationTransaction, Applicant
from .accounting_softwares.factory import get_accounting_software
from .constants import (
    INITIATED_STEP,
    BALANCE_SHEET_REQUESTED_STEP,
    RETRIEVED_BALANCE_SHEET_STEP,
    DECISION_REQUESTED_STEP,
    DECISION_RESULT_SENT_TO_USER_STEP,
)
from .serializers import LoanDetailsSerializer


def send_json_response(data, success=True, message="Success"):
    return Response({
        "data": data,
        "success": success,
        "message": message,
    })


def get_transaction_and_validate_against_user(transaction_id, request_user):
    if not transaction_id:
        return None, "Transaction ID is empty"

    transaction = LoanApplicationTransaction.objects.get(id=transaction_id)
    if request_user != transaction.applicant.user:
        return None, "Unauthorized access"

    return transaction, ""

class InitiateApplication(APIView):
    def post(self, request):
        applicant, _ = Applicant.objects.get_or_create(user=request.user)
        transaction = LoanApplicationTransaction(
            steps=INITIATED_STEP,
            applicant=applicant,
        )
        transaction.save()
        return send_json_response({'transaction_id': transaction.id})


class SaveLoanApplicationDetails(APIView):
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        transaction, error_message = get_transaction_and_validate_against_user(transaction_id, request.user)
        if transaction is None:
            return send_json_response({}, success=False, message=error_message)
        if transaction.steps != INITIATED_STEP:
            return send_json_response({}, success=False, message="Unable to execute this functionality with the current loan application step.")

        # TODO: Important to sanitize the input from client side before saving to db
        name = request.data.get('name', '')
        year_established = request.data.get('year_established', '')
        summary_of_profit_or_loss = request.data.get('summary_of_profit_or_loss', '')
        loan_amount = request.data.get('loan_amount', '')
        accounting_software_key = request.data.get('accounting_software_key', '')

        serializer = LoanDetailsSerializer(
            data={
                "name": name,
                "year_established": year_established,
                "summary_of_profit_or_loss": summary_of_profit_or_loss,
                "loan_amount": loan_amount,
                "accounting_software_key": accounting_software_key,
            }
        )
        if not serializer.is_valid():
            error_message = ",".join(serializer.custom_full_errors.get('errors', []))
            return send_json_response({}, success=False, message=error_message)

        transaction.set_application_details(serializer.validated_data)
        return send_json_response({})


class RequestBalanceSheet(APIView):
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        transaction, error_message = get_transaction_and_validate_against_user(transaction_id, request.user)
        if transaction is None:
            return send_json_response({}, success=False, message=error_message)
        if transaction.steps != INITIATED_STEP:
            return send_json_response({}, success=False, message="Unable to execute this functionality with the current loan application step.")
        
        accounting_software_key = transaction.get_application_details().get('accounting_software_key')
        accounting_software = get_accounting_software(accounting_software_key, transaction)
        if accounting_software is None:
            return send_json_response({}, success=False, message=f"Accounting software is not supported: {accounting_software}")

        transaction.steps = BALANCE_SHEET_REQUESTED_STEP
        transaction.save(update_fields=['steps'])

        balance_sheet, success = accounting_software.request_balance_sheet()
        if not success:
            return send_json_response({}, success=False, message=f"Error retrieving balance sheet. Please double check the credentials.")
        if not balance_sheet:
            return send_json_response({}, success=False, message=f"Balance sheet retrieved from ${accounting_software_key} is empty")

        transaction.steps = RETRIEVED_BALANCE_SHEET_STEP
        transaction.save(update_fields=['steps'])

        transaction.save_balance_sheet(balance_sheet)

        return send_json_response({"balance_sheet": balance_sheet})


class SubmitApplication(APIView):
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        transaction, error_message = get_transaction_and_validate_against_user(transaction_id, request.user)
        if transaction is None:
            return send_json_response({}, success=False, message=error_message)
        if transaction.steps != RETRIEVED_BALANCE_SHEET_STEP:
            return send_json_response({}, success=False, message="Unable to execute this functionality with the current loan application step.")

        transaction.steps = DECISION_REQUESTED_STEP
        transaction.save(update_fields=['steps'])

        # TODO: Create the pre-assessment logic and send to decision engine
        decision_outcome = "DECISION_OUTCOME"
        if not decision_outcome:
            return send_json_response({}, success=False, message="An error occurred when submitting the application. Please try again.")

        transaction.steps = DECISION_RESULT_SENT_TO_USER_STEP
        transaction.save(update_fields=['steps'])

        transaction.save_decision_outcome(decision_outcome)

        return send_json_response({'decision_outcome': decision_outcome})
