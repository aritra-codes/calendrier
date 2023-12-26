import datetime
import sys
import constants as c
import helpers as h


def main():
    args = h.setup_argparse(c.DESCRIPTION, c.POS_ARGS, c.ARGS)

    h.check_required_files()

    # Validates date inputted, if empty sets it to today
    date_args = [args.year, args.month, args.day]

    if not any(date_args):
        date = datetime.date.today()
    else:
        if args.view:
            date_args[2] = 1

        if not (date := h.validate_date_input(*date_args)):
            sys.exit("Input valid date.")

    if args.view:
        h.display_calendar(date.year, date.month)
    if args.event:
        h.return_events(date, True)
    if args.create:
        h.create_event(date)
    if args.delete:
        h.delete_event(date)
    if args.edit:
        h.edit_event(date)
    if args.pref:
        h.return_all_prefs(True)
    if args.changepref:
        h.change_pref()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nExitting application...")
