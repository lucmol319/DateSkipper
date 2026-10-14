"""
Utility functions for handling date calculations with a focus on business days and recurring dates.

Add business days by skipping weekends. Positive values add days, negative values subtract days.
""" 
from datetime import datetime, timedelta
from first_date_utilities import add_years_precise, add_months, add_weeks, add_days, parse_weekday

def add_business_days(start_date, business_days):
    if business_days == 0:
        return start_date

    current = start_date
    step = 1 if business_days > 0 else -1
    remaining = abs(int(business_days))

    while remaining > 0:
        current += timedelta(days=step)
        if current.weekday() < 5:
            remaining -= 1

    return current

# Find the next occurrence of a specified weekday after a given start date.
def next_weekday(start_date, weekday):
    weekday = parse_weekday(str(weekday))
    delta = (weekday - start_date.weekday() + 7) % 7
    if delta == 0:
        delta = 7
    return start_date + timedelta(days=delta)


def generate_recurring_dates(start_date, count, interval_type, interval_value):
    """
    Generate a list of recurring dates based on a start date, count, and interval.
    """
    dates = [start_date]
    current = start_date

    # Loop to generate the specified number of recurring dates based on the interval type and value.
    for _ in range(count - 1):
        if interval_type == "years":
            current = add_years_precise(current, interval_value)
        elif interval_type == "months":
            current = add_months(current, int(interval_value))
        elif interval_type == "weeks":
            current = add_weeks(current, interval_value)
        elif interval_type == "days":
            current = add_days(current, interval_value)
        else:
            raise ValueError("Unsupported interval type")
        dates.append(current)

    return dates


def read_start_date(prompt="Enter the starting date"):
    """
    Function to read a valid start date from user input.
    """
    while True:
        try:
            print(prompt)
            year = int(input("  Year (e.g., 2024): "))
            month = int(input("  Month (1-12): "))
            day = int(input("  Day (1-31): "))
            return datetime(year, month, day) # datetime object representing the start date
        except ValueError:
            print("Invalid date. Please try again.")

def choose_year_method():
    """
    Function to choose the year addition method.
    """
    method = input("Choose year method ('simple' or 'precise'): ").strip().lower()
    return "simple" if method == "simple" else "precise"