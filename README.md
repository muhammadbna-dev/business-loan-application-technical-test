# business-loan-application-system

# Architecture acceptance criteria
1. Important to record a sttus of the user's loan application such that if there was an error in any of the steps, they can start from that step rather than restarting the whole process
2. There are multiple accounting software to be integrated. Important to create a serializer to be able to transform the data from multiple accounting software to a standardized data format (Factory, Facade and Adapter pattern will work well here)


# Data architecture considerations
- LoanApplicationTransaction model containing
    - Steps:
        - INITIATED (Upon creation of transaction recor, no data is stored yet)
        - BALANCE_SHEET_REQUESTED (After first set of loan application fields are filled up and balance sheet is requested from accounting software)
        - RETRIEVED_BALANCE_SHEET (After retrieving balance sheet from accounting software)
        - APPLICATION_REVIEWED (After user reviewed application)
        - DECISION_REQUESTED (Application submitted to decision engine)
        - DECISION_RESULT_SENT_TO_USER (End state where user view decision result from decision engine)
