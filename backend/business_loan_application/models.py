from django.db import models
from django.contrib.auth.models import User

from .constants import BUSINESS_LOAN_STEPS


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


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
