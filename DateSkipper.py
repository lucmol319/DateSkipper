from datetime import datetime, timedelta
from py_compile import main
"""
Simple approach to add fractional years by converting the entire fraction into days
This method assumes an average year length of 365.25 days, which accounts for leap years
"""
def add_fractional_years(start_date, years):
    days_in_year = 365.25
    total_days = years * days_in_year
    return start_date + timedelta(days=total_days)

# 2028 is a leap year
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

"""
More precise approach (years + fraction separately)
Adds whole years properly
Converts the fractional part into days based on the resulting year
"""
def add_years_precise(start_date, years):
    whole_years = int(years)
    fractional_part = years - whole_years

    try:
        # Add whole years directly
        new_date = start_date.replace(year=start_date.year + whole_years)
    except ValueError:
        # Handles Feb 29 → Feb 28 on non-leap years
        new_date = start_date.replace(month=2, day=28, year=start_date.year + whole_years)

    # Convert fractional year to days
    days_in_year = 366 if is_leap_year(new_date.year) else 365
    extra_days = fractional_part * days_in_year

    return new_date + timedelta(days=extra_days)

# Defining main function
def main():
    # Loop to test the functions with a specific date and fractional years
    while True:
        # Input starting date (some error handling for invalid dates could be added here)
        year = int(input("Enter the starting year (e.g., 2024): "))
        month = int(input("Enter the starting month (1-12): "))
        day = int(input("Enter the starting day (1-31): "))

        wrongMonth = month < 1 or month > 12 # 1 < month < 12
        wrongDay = day < 1 or day > 31 # 1 < day < 31
        
        if wrongMonth or wrongDay:
            print("Invalid date. Please try again.")
            continue

        start = datetime(year, month, day)

        # Input years to add as a fraction (e.g., 3.67 for 3 years and 2/3 of a year)
        years_to_add = float(input("Enter the number of years to add (can be fractional, e.g., 3.67): "))

        # Do you want simple or precise method?
        method = input("Choose method ('simple' or 'precise'): ")

        if method == "simple":
            new_date = add_fractional_years(start, years_to_add)
        else:
            new_date = add_years_precise(start, years_to_add)

        print("Start date:", start.strftime("%m/%d/%Y"))
        print("New date:", new_date.strftime("%m/%d/%Y"))

        runAgain = input("Press Enter to run again...")
        if runAgain != "":
            break

if __name__=="__main__":
    main()
