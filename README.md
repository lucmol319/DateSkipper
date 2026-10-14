# DateSkipper

DateSkipper is an interactive Python command-line tool for calculating dates and times. Enter a starting date, choose an operation, and the program prints the result. It is useful for exploring date offsets, comparing dates, and generating simple recurring schedules.

## What it can do

- Add years using either an average-year method (365.25 days per year) or a calendar-aware method that applies whole years first and converts the fractional part using the length of the resulting year.
- Add months, weeks, days, or hours/minutes/seconds. Month arithmetic adjusts to the last day of the target month when needed.
- Apply a composite interval of years, months, weeks, days, and time.
- Find the difference between two dates in years, months, and days, as well as total days and weeks.
- Add or subtract business days by skipping Saturdays and Sundays. Holidays are not currently considered.
- Find the next occurrence of a weekday, entered as a name or as a number from `0` (Monday) to `6` (Sunday).
- Generate a sequence of dates at a chosen yearly, monthly, weekly, or daily interval.

The program uses Python's standard library and does not require third-party packages.

## How it works

`DateSkipper.py` displays a numbered menu and gathers the values needed for the selected operation. It reads dates as separate year, month, and day values, then delegates calculations to utility functions:

- `first_date_utilities.py` implements date arithmetic, weekday parsing, leap-year checks, and date differences.
- `second_date_utilities.py` implements business-day arithmetic, next-weekday lookup, recurring dates, and interactive date/method prompts.
- `constants.py` contains the weekday names shared by the utilities.

Date calculations use Python's `datetime` and `timedelta` types. The “simple” fractional-year method treats every year as 365.25 days. The “precise” method preserves calendar-year boundaries for the whole-number portion, then uses the length of the resulting year for the fractional portion; it is a practical convention rather than a universal definition of a fractional year.

## Project layout

```text
DateSkipper/
├── DateSkipper.py              # Interactive menu and program entry point
├── first_date_utilities.py     # Core date and time calculations
├── second_date_utilities.py    # Business days, weekdays, and recurrence
├── constants.py                # Shared weekday names
└── README.md                   # Project guide
```

## Run it yourself

Install Python 3 if it is not already installed. From the project directory, run:

```powershell
python DateSkipper.py
```

On Windows, if the Python launcher is available, you can use `py` instead:

```powershell
py DateSkipper.py
```

No dependency installation is needed. Follow the prompts in the menu to choose an operation and enter its inputs. Choose **11) Quit** to exit.

### Optional virtual environment

To run the project in an isolated Python environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python DateSkipper.py
```

## Current scope

DateSkipper currently runs in a terminal and accepts dates as year/month/day components. It does not yet provide a graphical or web interface, command-line flags, date-string parsing, holiday calendars, or timezone-aware calculations.

## Future Feature Checklist

4. Add calendar and date info
- Show weekday name, ISO week number, quarter, day-of-year
- Determine whether a date is in a leap year
- Find the start/end of the month, quarter, or year
5. Add event and schedule utilities
- Generate recurring event dates (weekly, monthly, yearly)
- Build a schedule of dates from a start date + recurrence rule
- Find the next occurrence of a given weekday
6. Add input/output improvements
- Parse dates from strings like 2024-12-31 or Dec 31 2024
- Validate dates properly instead of only checking month/day ranges
- Save results to a file or CSV
- Add command-line arguments so it can be used non-interactively
7. Add time and timezone support
- Switch from datetime to datetime with time-of-day
- Add time zone awareness using pytz or zoneinfo
- Compute date-time offsets precisely
8. Add precision and domain-specific calculations
- Add exact month fraction handling
- Add “business age” or “school year” calculations
- Add astronomical or fiscal-period calculations
9. Improve usability
- Provide menu options for different operations
- Add a “help” command or usage guide
- Keep the program running until the user chooses to quit

Extras:
- Turn it into a website that manages these features with buttons and other FX assets.