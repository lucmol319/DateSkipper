from datetime import datetime, timedelta
from calendar import monthrange
"""
cd "c:/Users/lucmo/Documents/My GitHub Repositories/DateSkipper/.venv/Scripts/python.exe" -m py_compile DateSkipper.py
cd "c:/Users/lucmo/Documents/My GitHub Repositories/DateSkipper/.venv/Scripts/python.exe" DateSkipper.py
Feature checklist:
4. Add calendar and date info
Show weekday name, ISO week number, quarter, day-of-year
Determine whether a date is in a leap year
Find the start/end of the month, quarter, or year
5. Add event and schedule utilities
Generate recurring event dates (weekly, monthly, yearly)
Build a schedule of dates from a start date + recurrence rule
Find the next occurrence of a given weekday
6. Add input/output improvements
Parse dates from strings like 2024-12-31 or Dec 31 2024
Validate dates properly instead of only checking month/day ranges
Save results to a file or CSV
Add command-line arguments so it can be used non-interactively
7. Add time and timezone support
Switch from datetime to datetime with time-of-day
Add time zone awareness using pytz or zoneinfo
Compute date-time offsets precisely
8. Add precision and domain-specific calculations
Add exact month fraction handling
Add “business age” or “school year” calculations
Add astronomical or fiscal-period calculations
9. Improve usability
Provide menu options for different operations
Add a “help” command or usage guide
Keep the program running until the user chooses to quit
"""

"""
Simple approach to add fractional years by converting the entire fraction into days.
This method assumes an average year length of 365.25 days, which accounts for leap years.
"""
def add_fractional_years(start_date, years):
    days_in_year = 365.25
    total_days = years * days_in_year
    return start_date + timedelta(days=total_days)

# 2028 is a leap year
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

"""
More precise approach (years + fraction separately).
Adds whole years properly and converts the fractional part to days based
on the resulting year.
"""
def add_years_precise(start_date, years):
    whole_years = int(years)
    fractional_part = years - whole_years

    try:
        new_date = start_date.replace(year=start_date.year + whole_years)
    except ValueError:
        new_date = start_date.replace(month=2, day=28, year=start_date.year + whole_years)

    days_in_year = 366 if is_leap_year(new_date.year) else 365
    extra_days = fractional_part * days_in_year

    return new_date + timedelta(days=extra_days)

"""
Add integer months to a date and adjust the day if the target month
has fewer days than the source date.
"""
def add_months(start_date, months):
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

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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

# Add business days by skipping weekends. Positive values add days, negative values subtract days.
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

# Generate a list of recurring dates based on a start date, count, and interval.
def generate_recurring_dates(start_date, count, interval_type, interval_value):
    dates = [start_date]
    current = start_date

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

# Function to read a valid start date from user input.
def read_start_date(prompt="Enter the starting date"):
    while True:
        try:
            print(prompt)
            year = int(input("  Year (e.g., 2024): "))
            month = int(input("  Month (1-12): "))
            day = int(input("  Day (1-31): "))
            return datetime(year, month, day)
        except ValueError:
            print("Invalid date. Please try again.")

# Function to choose the year addition method.
def choose_year_method():
    method = input("Choose year method ('simple' or 'precise'): ").strip().lower()
    return "simple" if method == "simple" else "precise"

# Main loop to interact with the user and perform date calculations based on their choices.
def main():
    while True:
        print("\nDateSkipper: date utilities")
        print("1) Add years")
        print("2) Add months")
        print("3) Add weeks")
        print("4) Add days")
        print("5) Add hours/minutes/seconds")
        print("6) Add a composite interval")
        print("7) Date difference")
        print("8) Add business days")
        print("9) Next weekday")
        print("10) Generate recurring dates")
        print("11) Quit")

        choice = input("Choose an option (1-11): ").strip()
        if choice == "11":
            break

        if choice == "7":
            start = read_start_date("Enter the first date")
            end = read_start_date("Enter the second date")
            diff = date_difference(start, end)
            print("Start date:", start.strftime("%Y-%m-%d"))
            print("End date:", end.strftime("%Y-%m-%d"))
            print(f"Difference: {diff['years']} years, {diff['months']} months, {diff['days']} days")
            print(f"Total: {diff['total_days']} days ({diff['total_weeks']} weeks and {diff['remaining_days']} days)")
            if diff['swapped']:
                print("(Dates were entered in reverse order.)")
            continue

        start = read_start_date()
        new_date = start

        if choice == "1":
            years_to_add = float(input("Enter the number of years to add (can be fractional, e.g., 3.67): "))
            method = choose_year_method()
            new_date = add_fractional_years(start, years_to_add) if method == "simple" else add_years_precise(start, years_to_add)
        elif choice == "2":
            months_to_add = int(input("Enter the number of months to add: "))
            new_date = add_months(start, months_to_add)
        elif choice == "3":
            weeks_to_add = float(input("Enter the number of weeks to add: "))
            new_date = add_weeks(start, weeks_to_add)
        elif choice == "4":
            days_to_add = float(input("Enter the number of days to add: "))
            new_date = add_days(start, days_to_add)
        elif choice == "5":
            hours = float(input("Enter hours to add: "))
            minutes = float(input("Enter minutes to add: "))
            seconds = float(input("Enter seconds to add: "))
            new_date = add_time(start, hours=hours, minutes=minutes, seconds=seconds)
        elif choice == "6":
            years_to_add = float(input("Enter years to add (can be fractional, or 0): "))
            method = choose_year_method()
            months_to_add = int(input("Enter the number of months to add: "))
            weeks_to_add = float(input("Enter the number of weeks to add: "))
            days_to_add = float(input("Enter the number of days to add: "))
            hours = float(input("Enter hours to add: "))
            minutes = float(input("Enter the number of minutes to add: "))
            seconds = float(input("Enter the number of seconds to add: "))

            new_date = add_fractional_years(start, years_to_add) if method == "simple" else add_years_precise(start, years_to_add)
            new_date = add_months(new_date, months_to_add)
            new_date = add_weeks(new_date, weeks_to_add)
            new_date = add_days(new_date, days_to_add)
            new_date = add_time(new_date, hours=hours, minutes=minutes, seconds=seconds)
        elif choice == "8":
            business_days = int(input("Enter business days to add (positive or negative): "))
            new_date = add_business_days(start, business_days)
        elif choice == "9":
            weekday_text = input("Enter the next weekday (0=Mon .. 6=Sun or name): ")
            new_date = next_weekday(start, weekday_text)
        elif choice == "10":
            count = int(input("How many recurring dates should be generated? "))
            interval_type = input("Interval type ('years', 'months', 'weeks', 'days'): ").strip().lower()
            interval_value = float(input("Interval value: "))
            dates = generate_recurring_dates(start, count, interval_type, interval_value)
            print("Recurring dates:")
            for date_item in dates:
                print(" -", date_item.strftime("%Y-%m-%d %H:%M:%S"))
            continue
        else:
            print("Invalid option. Please choose a number from 1 to 11.")
            continue

        print("Start date:", start.strftime("%Y-%m-%d %H:%M:%S"))
        print("Result:", new_date.strftime("%Y-%m-%d %H:%M:%S"))

        again = input("Press Enter to run again, or type 'q' to quit: ").strip().lower()
        if again == "q":
            break

if __name__ == "__main__":
    main()