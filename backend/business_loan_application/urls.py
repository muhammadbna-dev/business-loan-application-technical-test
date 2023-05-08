from django.urls import path

from .views import (
    InitiateApplication,
    SaveLoanApplicationDetails,
    RequestBalanceSheet,
    SubmitApplication,
)

urlpatterns=[
  path('initiate-application/', InitiateApplication.as_view()),
  path('save-loan-application-details/', SaveLoanApplicationDetails.as_view()),
  path('request-balance-sheet/', RequestBalanceSheet.as_view()),
  path('submit-application/', SubmitApplication.as_view()),
]
