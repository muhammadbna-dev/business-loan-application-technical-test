from abc import ABC, abstractmethod

'''
Abstract base class to ensure that any other accounting software that we integrate with will 
always have the core functions that is neede for the feature integration to work.
'''


class BaseAdapter(ABC):
    def __init__(self, loan_application_transaction):
        self.loan_application_transaction = loan_application_transaction

    @abstractmethod
    def _get_credentials(self):
        pass

    @abstractmethod
    def request_balance_sheet(self):
        pass
