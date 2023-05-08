from datetime import datetime


def _sort_balance_sheet_from_most_recent_to_least(balance_sheet):
    # Add an estimated date so that its easier to sort from most recent to least recent items in balance sheet
    new_balance_sheet = []
    for item in balance_sheet:
        month = item['month']
        if month > 9:
            month = str(month)
        else:
            month = f"0{month}"
        item['estimated_date'] = f"01/{month}/{item['year']}"
        new_balance_sheet.append(item)

    return sorted(
        new_balance_sheet,
        key=lambda item: datetime.strptime(item['estimated_date'], "%d/%m/%Y"),
        reverse=True
    ) 


def _generate_pre_assessment_value(balance_sheet, loan_amount):
    # NOTE: This function assumes that the balance sheet has a record of every month i.e. no missing months

    sorted_balance_sheet = _sort_balance_sheet_from_most_recent_to_least(balance_sheet)
    recent_12_months_items = sorted_balance_sheet[0:12]

    has_made_profit_in_last_12_months = True
    for item in recent_12_months_items:
        if item['profit_or_loss'] <= 0:
            has_made_profit_in_last_12_months = False
            break
    
    if has_made_profit_in_last_12_months:
        return "60"

    average_asset_value_in_12_months_more_than_loan_amount = True
    overall_assets_value = 0
    for item in recent_12_months_items:
        overall_assets_value += item['assets_value']
    
    average_assets_value = overall_assets_value / 12

    if average_assets_value > float(loan_amount):
        return "100"

    return "20"


def _call_decision_engine_api_stub(pre_assessment_value, name, year_established, summary_of_profit_or_loss):
    '''
    NOTE: In actuality, the retrieval of the credentials, URL, transforming request and response data will be handled here.
    This implementation makes the assumption that there is only one decision engine.
    Assuming if there are multiple decision engines to select from, the architecture and implementation will follow the accounting software adapters.
    '''
    return "DECISION OUTCOME"


def get_decision_outcome(transaction):
    balance_sheet = transaction.get_balance_sheet()
    application_details = transaction.get_application_details()
    name = application_details['name']
    year_established = application_details['year_established']
    summary_of_profit_or_loss = application_details['summary_of_profit_or_loss']
    loan_amount = application_details['loan_amount']

    pre_assessment_value = _generate_pre_assessment_value(balance_sheet, loan_amount)
    transaction.save_pre_assessment_value(pre_assessment_value)

    decision_outcome = _call_decision_engine_api_stub(pre_assessment_value, name, year_established, summary_of_profit_or_loss)
    transaction.save_decision_outcome(decision_outcome)
    return decision_outcome
