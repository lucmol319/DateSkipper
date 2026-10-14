"""
Utility functions for handling date calculations with a focus on business days and recurring dates.
Add business days by skipping weekends. Positive values add days, negative values subtract days.
"""
from calendar import monthrange
from datetime import timedelta
from constants import WEEKDAY_NAMES

def add_fractional_years(start_date, years):
    """
    Simple approach to add fractional years by converting the entire fraction into days.
    This method assumes an average year length of 365.25 days, which accounts for leap years.
    """
    days_in_year = 365.25
    total_days = years * days_in_year
    return start_date + timedelta(days=total_days)

# 2028 is a leap year
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def add_years_precise(start_date, years):
    """
    More precise approach (years + fraction separately).
    Adds whole years properly and converts the fractional part to days based
    on the resulting year.
    """
    whole_years = int(years)
    fractional_part = years - whole_years

    try:
        new_date = start_date.replace(year=start_date.year + whole_years)
    except ValueError:
        new_date = start_date.replace(month=2, day=28, year=start_date.year + whole_years)

    days_in_year = 366 if is_leap_year(new_date.year) else 365
    extra_days = fractional_part * days_in_year

    return new_date + timedelta(days=extra_days)


def add_months(start_date, months):
    """
    Add integer months to a date and adjust the day if the target month
    has fewer days than the source date.
    """
    if months == 0:
        return start_date

    total_months = start_date.month - 1 + months
    new_year = start_date.year + total_months // 12
    new_month = total_months % 12 + 1
    new_day = min(start_date.day, monthrange(new_year, new_month)[1])

    return start_date.replace(year=new_year, month=new_month, day=new_day)


# Add weeks, days, and time intervals using timedelta.
def add_weeks(start_date, weeks):
    return start_date + timedelta(weeks=weeks)

# Add days (can be fractional) using timedelta.
def add_days(start_date, days):
    return start_date + timedelta(days=days)

# Add hours, minutes, and seconds using timedelta.
def add_time(start_date, hours=0, minutes=0, seconds=0):
    return start_date + timedelta(hours=hours, minutes=minutes, seconds=seconds)


# Parse weekday input which can be either a number (0-6) or a name (e.g., "Monday").
def parse_weekday(text):
    text = text.strip().lower()
    if text.isdigit():
        value = int(text)
        if 0 <= value <= 6:
            return value
    for index, name in enumerate(WEEKDAY_NAMES):
        if text == name.lower() or text == name[:3].lower():
            return index
    raise ValueError("Weekday must be 0-6 or a weekday name")

# Calculate the difference between two dates in years, months, days, and total days/weeks.
def date_difference(start_date, end_date):
    swapped = False
    if start_date > end_date:
        start_date, end_date = end_date, start_date
        swapped = True

    years = end_date.year - start_date.year
    months = end_date.month - start_date.month
    days = end_date.day - start_date.day

    if days < 0:
        months -= 1
        prev_month = end_date.month - 1 or 12
        prev_year = end_date.year if end_date.month != 1 else end_date.year - 1
        days += monthrange(prev_year, prev_month)[1]

    if months < 0:
        years -= 1
        months += 12

    total_days = abs((end_date - start_date).days)
    total_weeks = total_days // 7
    remaining_days = total_days % 7

    return {
        "years": years,
        "months": months,
        "days": days,
        "total_days": total_days,
        "total_weeks": total_weeks,
        "remaining_days": remaining_days,
        "swapped": swapped,
    }