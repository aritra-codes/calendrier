DEFAULT_ENCODING = "utf-8"

# Argument parser
ON_OFF_ACTION = "store_true"
DESCRIPTION = "View and create events on a calendar."


class Arg:
    def __init__(self, short, long, action, arg_help=""):
        self.short = short
        self.long = long
        self.action = action
        self.help = arg_help


class PosArg:
    def __init__(self, name, arg_help="", optional=True):
        self.name = name
        self.help = arg_help
        self.optional = optional


ARGS = [
    Arg("v", "view", ON_OFF_ACTION, "View the calendar"),
    Arg("e", "event", ON_OFF_ACTION, "Views events on a specific date"),
    Arg("c", "create", ON_OFF_ACTION, "Create an event"),
    Arg("d", "delete", ON_OFF_ACTION, "Delete an event"),
    Arg("ed", "edit", ON_OFF_ACTION, "Edit an event"),
    Arg("p", "pref", ON_OFF_ACTION, "View all preferences"),
    Arg("cp", "changepref", ON_OFF_ACTION, "Change a preference")
]
POS_ARGS = [
    PosArg("year", "Year to use, defaults to today"),
    PosArg("month", "Month to use, defaults to today"),
    PosArg("day", "Day to use, defaults to today")
]

# Dates
SUNDAY_OFFSET = [6, 0, 1, 2, 3, 4, 5]
WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]
WEEKDAYS_SHORT = [weekday[0:3] for weekday in WEEKDAYS]
MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]
CALENDAR_TABLE_FORMAT = {weekday: [] for weekday in WEEKDAYS}
TODAY_ON_COLOR = "on_cyan"

# Events
EVENTS_FILE_LOCATION = "events.csv"
EVENTS_DATE_KEY = "date"
EVENTS_NAME_KEY = "name"
EVENTS_FILE_FIELDNAMES = [EVENTS_DATE_KEY, EVENTS_NAME_KEY]

# Settings
SETTINGS_FILE_LOCATION = "settings.ini"
PREFS_SECTION_NAME = "PREFERENCES"


class Pref:
    def __init__(self, name, default):
        self.name = name
        self.default = default


SUNDAY_FIRST_PREF = Pref("sunday_first", "false")
SHORT_WEEKDAYS_PREF = Pref("short_weekdays", "true")
TABLE_FORMAT_PREF = Pref("table_format", "rounded_grid")

DEFAULT_PREFS = {pref.name: pref.default
                 for pref in [SUNDAY_FIRST_PREF, SHORT_WEEKDAYS_PREF, TABLE_FORMAT_PREF]}
