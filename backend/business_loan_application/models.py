from django.db import models
from django.contrib.auth.models import User

from .constants import BUSINESS_LOAN_STEPS


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


'''
NOTE: application_details field is a super field where many data fields are stored.
It's implemented as such because there may be many fields that are needed for the loan application and i do not have the
domain knowledge to know what fields are important and will be changed. 
In reality, a proper discussion will be done with domain experts to understand what fields are necessary that needs to
be added as db table columns and not just a JSON field
'''


class LoanApplicationTransaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    steps = models.CharField(
        max_length=50,
        choices=BUSINESS_LOAN_STEPS,
    )
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    application_details = models.JSONField(default=dict)

    def get_application_details(self):
         self.refresh_from_db()
         return self.application_details

    def set_application_details(self, application_details):
        self.application_details = application_details
        self.save(update_fields=['application_details'])

    def get_balance_sheet(self):
        self.refresh_from_db()
        return self.get_application_details().get('balance_sheet' , [])

    def save_balance_sheet(self, balance_sheet):
        self.refresh_from_db()
        self.application_details['balance_sheet'] = balance_sheet
        self.save(update_fields=['application_details'])

    def get_decision_outcome(self):
        self.refresh_from_db()
        return self.get_application_details().get('decision_outcome' , '')

    def save_decision_outcome(self, decision_outcome):
        self.refresh_from_db()
        self.application_details['decision_outcome'] = decision_outcome
        self.save(update_fields=['application_details'])

    def get_pre_assessment_value(self):
        self.refresh_from_db()
        return self.get_application_details().get('pre_assessment_value' , '')

    def save_pre_assessment_value(self, pre_assessment_value):
        self.refresh_from_db()
        self.application_details['pre_assessment_value'] = pre_assessment_value
        self.save(update_fields=['application_details'])

    def get_decision_outcome(self):
        self.refresh_from_db()
        return self.get_application_details().get('decision_outcome' , '')

    def save_decision_outcome(self, decision_outcome):
        self.refresh_from_db()
        self.application_details['decision_outcome'] = decision_outcome
        self.save(update_fields=['application_details'])
