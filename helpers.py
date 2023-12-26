from argparse import ArgumentParser
import datetime
from calendar import monthrange
from configparser import ConfigParser, NoSectionError, NoOptionError
import csv
from tabulate import tabulate
from termcolor import colored
import constants as c


def rewrite_csv_file(location, fieldnames, rows=None):
    if rows is None:
        rows = []

    with open(location, "w", newline="", encoding=c.DEFAULT_ENCODING) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def return_all_rows(location):
    with open(location, encoding=c.DEFAULT_ENCODING) as file:
        reader = csv.DictReader(file)

        return list(reader)


# Makes sure an input is not blank
def validate_input(name, value=""):
    if value:
        return value

    while True:
        inp = input(f"Input {name}: ")

        if not inp:
            print("Must not be blank.")
            continue

        break

    return inp


def validate_date_input(year, month, day):
    try:
        return datetime.date(int(year), int(month), int(day))
    except (ValueError, TypeError):
        return False


def setup_argparse(description, pos_args, args):
    p = ArgumentParser(
        description=description)

    for arg in args:
        p.add_argument(f"-{arg.short}", f"--{arg.long}", action=arg.action, help=arg.help)

    for arg in pos_args:
        p.add_argument(arg.name, help=arg.help, nargs="?" if arg.optional else None)

    return p.parse_args()


# Checks for required files and creates them if necessary
def check_required_files():
    check_events_file()
    check_settings_file()


def check_events_file(location=None, fieldnames=None):
    if location is None:
        location = c.EVENTS_FILE_LOCATION
    if fieldnames is None:
        fieldnames = c.EVENTS_FILE_FIELDNAMES

    try:
        with open(location, encoding=c.DEFAULT_ENCODING) as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != fieldnames:
                raise NameError
    except (FileNotFoundError, NameError):
        rewrite_events_file()
        print("Recreated events.csv.")


def display_calendar(year, month):
    day_table = [[] for _ in range(7)]
    max_day = monthrange(year, month)[1]

    today = datetime.date.today()

    # Iterates through all the days in the month and assigns each to the correct weekday in the day_table
    for day in range(1, max_day + 1):
        current_date = datetime.date(year, month, day)
        current_weekday = current_date.weekday()

        # If the current date is today then it will be colored
        cell = str(colored(day, on_color=c.TODAY_ON_COLOR) if current_date == today else day)

        events = return_events(current_date)
        for event in events:
            cell += f"\n • {event.get("name")}"

        day_table[current_weekday].append(cell)

    # Makes a dictionary with the weekday name as the key and the days falling on that weekday as the value
    sunday_pref = get_pref(c.SUNDAY_FIRST_PREF, True)
    short_pref = get_pref(c.SHORT_WEEKDAYS_PREF, True)

    weekdays = c.WEEKDAYS_SHORT if short_pref else c.WEEKDAYS

    calendar = {weekday: day_table[index] for index, weekday in enumerate(weekdays)}

    # Offsets the calendar dictionary by 1 so Sunday is the first day
    if sunday_pref:
        edited_calendar = {}

        for i in c.SUNDAY_OFFSET:
            weekday = weekdays[i]

            edited_calendar[weekday] = calendar[weekday]

        calendar = edited_calendar

    # Empties the spaces before the first day of the month
    first_weekday = datetime.date(year, month, 1).weekday()
    if sunday_pref:
        first_weekday = c.SUNDAY_OFFSET.index(first_weekday)
    keys = calendar.keys()
    for key in list(keys)[:first_weekday]:
        calendar[key].insert(0, None)

    print(f"{c.MONTHS[month - 1]} {year}:")
    print(tabulate(calendar, headers="keys", tablefmt=get_pref(c.TABLE_FORMAT_PREF)))


def does_event_exist(event):
    return event in return_events()


def create_event(date):
    name = validate_input("event name")

    # Writes the event into the events csv file
    with open(c.EVENTS_FILE_LOCATION, "a", newline="", encoding=c.DEFAULT_ENCODING) as file:
        writer = csv.DictWriter(file, fieldnames=c.EVENTS_FILE_FIELDNAMES)

        event = {c.EVENTS_DATE_KEY: date.isoformat(), c.EVENTS_NAME_KEY: name}

        if does_event_exist(event):
            print("Event already exists.")
            return False

        writer.writerow(event)

    print(f"Successfully created event {name} on {date}!")


def return_events(date=None, display=False):
    events = return_all_rows(c.EVENTS_FILE_LOCATION)

    if date:
        events = [event
                  for event in events.copy()
                  if datetime.date.fromisoformat(event.get("date")) == date]

    if display:
        if events:
            if date:
                print(f"Events on {date}{" (today)" if date == date.today() else ""}:")

            print(tabulate(enumerate(event.get("name") for event in events),
                           headers=["ID", "Event"],
                           tablefmt="rounded_grid"))
        else:
            print("No events found on specified date.")

    return events


def select_event(date):
    if not (events := return_events(date, True)):
        return False

    while True:
        try:
            i = int(validate_input("ID"))
        except ValueError:
            print("Must an integer.")
        else:
            if 0 <= i < len(events):
                return events[i]
            print("Must be a valid ID.")


def rewrite_events_file(events=None):
    return rewrite_csv_file(c.EVENTS_FILE_LOCATION, c.EVENTS_FILE_FIELDNAMES, events)


# Rewrites the events csv file so the selected event is deleted
def delete_event(date):
    edited_events = return_events()

    if not (selected_event := select_event(date)):
        return False

    edited_events.remove(selected_event)

    rewrite_events_file(edited_events)

    print(f"Successfully deleted event on {date}!")


def edit_event(date):
    edited_events = return_events()

    if not (selected_event := select_event(date)):
        return False

    while True:
        match validate_input("Change date or name? (d/n)"):
            case "date" | "d":
                new_key = c.EVENTS_DATE_KEY

                while True:
                    new_value = validate_input("new date (e.g. 2000-12-24)")

                    try:
                        datetime.date.fromisoformat(new_value)
                    except ValueError:
                        print("Must be in YYYY-MM-DD format.")
                    else:
                        break
                break
            case "name" | "n":
                new_key = c.EVENTS_NAME_KEY
                new_value = validate_input("new event name")

                break

    edited_events[edited_events.index(selected_event)][new_key] = new_value

    rewrite_events_file(edited_events)

    print(f"Successfully edited {new_key} to {new_value}!")


def check_settings_file(location=c.SETTINGS_FILE_LOCATION,
                        prefs_section_name=c.PREFS_SECTION_NAME,
                        pref_names=c.DEFAULT_PREFS.keys()):
    config = ConfigParser()

    # Checks if the settings file exists
    if config.read(location):
        try:
            # Checks if pref section and every pref exists
            for pref in pref_names:
                if not config.get(prefs_section_name, pref):
                    raise ValueError
        except (NoSectionError, NoOptionError, ValueError):
            pass
        else:
            return

    rewrite_settings_file()
    print("Recreated settings.ini.")


def rewrite_settings_file(config=None):
    if not config:
        config = ConfigParser()
        config[c.PREFS_SECTION_NAME] = c.DEFAULT_PREFS

    with open(c.SETTINGS_FILE_LOCATION, "w", encoding=c.DEFAULT_ENCODING) as file:
        config.write(file)


def get_pref(pref, is_bool=False):
    config = ConfigParser()
    config.read(c.SETTINGS_FILE_LOCATION)

    kwargs = {"section": c.PREFS_SECTION_NAME, "option": pref.name, "fallback": pref.default}

    pref = config.getboolean(**kwargs) if is_bool else config.get(**kwargs)

    return pref


def return_all_prefs(display=False):
    config = ConfigParser()
    config.read(c.SETTINGS_FILE_LOCATION)
    prefs = config.items(c.PREFS_SECTION_NAME)

    table = []
    for i, pref in enumerate(prefs):
        table.append([i, pref[0], pref[1]])

    if display:
        print(tabulate(table,
                       headers=["ID", "Preference", "Value"],
                       tablefmt=get_pref(c.TABLE_FORMAT_PREF)))

    return prefs


def change_pref():
    prefs = return_all_prefs(True)

    while True:
        i = int(validate_input("ID"))

        if 0 <= i < len(prefs):
            selected_pref_name = prefs[i][0]
            break

    new_value = validate_input("new value")

    config = ConfigParser()
    config.read(c.SETTINGS_FILE_LOCATION)
    config.set(c.PREFS_SECTION_NAME, str(selected_pref_name), new_value)

    rewrite_settings_file(config)

    print(f"Successfully changed {selected_pref_name} to {new_value}!")
