from datetime import datetime
from dateutil.relativedelta import relativedelta

def return_current_month_plus_next_months(next_months):
    current_date = datetime.now()
    return current_date - relativedelta(months=next_months)
