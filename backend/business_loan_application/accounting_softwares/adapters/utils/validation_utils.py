from datetime import date

'''
Common validations for data fields irregardless of where the data fields were originated from (different accounting softwares)
'''

class DataValidationError(Exception):
    pass


def validate_year(year):
    year = int(year)

    if year > date.today().year:
        raise DataValidationError(f"Year received is more than current year. Year: {year}")
    if year <= 0:
        raise DataValidationError(f"Year received is 0 or negative. Year: {year}")
    
    return year

def validate_month(month):
    month = int(month)
    if month <= 0 or month > 12:
        raise DataValidationError(f"Invalid month. Month: {month}")

    return month
    
def validate_profit_or_loss(profit_or_loss):
    profit_or_loss = float(profit_or_loss)
    return profit_or_loss

def validate_assets_value(assets_value):
    assets_value = float(assets_value)
    return assets_value
