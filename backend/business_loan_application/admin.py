from django.contrib import admin

from .models import Applicant, LoanApplicationTransaction

admin.site.register(Applicant)
admin.site.register(LoanApplicationTransaction)
