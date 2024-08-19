"""
Utility module for date calculations.

This module provides functions to perform date-related operations, including calculating
dates based on the current month and a specified number of months to add or subtract.

Functions:
- return_current_month_plus_next_months: Calculates the date for the current month minus
  a specified number of months.
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta

def return_current_month_plus_next_months(next_months):
    """
    Calculates the date for the current month minus a specified number of months.

    Args:
        next_months (int): The number of months to subtract from the current date.

    Returns:
        datetime: 
            The resulting date after subtracting the specified number of months from the current
            date.
    """
    current_date = datetime.now()
    return current_date - relativedelta(months=next_months)
