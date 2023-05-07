from .validation_utils import (
    validate_year,
    validate_month,
    validate_profit_or_loss,
    validate_assets_value,
)


'''
Serializer to ensure that no matter what accounting software we integrate with (which all have their own unique data formats),
we serialize it to a consistent data format for this application.
'''


def serialize_balance_sheet_data(year, month, profit_or_loss, assets_value):
    return {
        'year': validate_year(year),
        'month': validate_month(month),
        'profit_or_loss': validate_profit_or_loss(profit_or_loss),
        'assets_value': validate_assets_value(assets_value),
    }
