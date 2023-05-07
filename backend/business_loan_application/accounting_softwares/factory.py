import logging

from .constants import (
    MYOB,
)
from .adapters.myob import MyobAdapter

# Note: Simple factory pattern to ensure that the core business logic of the system
# does not need to worry itself with the details of the adapter (accounting software)

def get_accounting_software(software_key, loan_application_transaction):
    accounting_softwares = {
        MYOB: MyobAdapter,
    }

    try:
        adapter = accounting_softwares[software_key]
        return adapter(loan_application_transaction)
    except KeyError:
        logging.exception(f"Accounting software is not supported: {software_key}")
        return None
