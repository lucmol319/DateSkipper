from first_date_utilities import(
    add_fractional_years, add_years_precise,
    add_months, parse_weekday, add_weeks, add_days, add_time, date_difference
)
from second_date_utilities import(
    add_business_days, next_weekday, generate_recurring_dates,
    read_start_date, choose_year_method
)

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
            years_to_add = float(input("Enter the number of years to add (can be fractional, ex: 3.67): "))
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