# Calendrier

#### This is my submission for the final project of CS50x 💻.

#### !! Not continuing work on this project (for now) !!

#### Calendrier 🗓️ is a command-line calendar application that helps you remember events. You can view, create, delete and edit events on specific days. Additionally, you can also customise your experience (a little bit).

![Command-line calendar view](/images/calendar.png)

---

## Journey and Decisions

As a beginner, the python apps that I have developed hitherto have been done in a single file. However this is a very bad practice for several reasons: functions cannot be reused in other projects, the file will be very messy and hard to read, etc. So I decided to use a much more known project structure where there is a file for the constants (constants.py), the helper functions (helpers.py) and running the app itself (main.py).

I used the python module argparse, so my app can easily be used in the terminal. This also automatically created a help page which will most definitely be useful for new users. I used this approach instead of just having the user run the app and get prompted for inputs because it is much faster and provides a better user experience.

Regarding the events themselves, I made it so you can either view all the events in a month on the calendar or you can view the events on a specific day. Also, if month shown in the calendar includes today or the events being displayed are today's, then there will be a visual indicator to remind the user that it is today. You can create an event on any day with any name. If you were to make a mistake during this process, you can either delete or edit the event. Deleting it is self-explanatory. If you were to edit it, you can either change the date or name of the event. All the events are stored in [events.csv](/events.csv), with each row (except the first which are the fieldnames/headers) containing an event's date and name.

I found that is would be ideal to allow the user to customise their experience. So I made options to allow the user to change whether Sunday should be the first day of the week (as it is in some parts of th world), whether they want the shortened weekday names to be displayed (so it is easier to read) and how the table used for the calendar and other lists looked (made possible by the different table formats provided by the python tabulate module). All the preferences are stored in [settings.ini](/settings.ini), with all the options under the PREFERENCES section.

All the inputs and options to run the program also have validation processes, so no invalid input is processed. If any of the required data files were to removed or tampered with, the app will automatically remake the file.

Finally, I ran pylint on all the code to try make sure there are as less bad practices as possible. I was able to find several bad practices which I fixed, but I didn't fix all of them.

I used [pipreqs](https://pypi.org/project/pipreqs/) to create [requirements.txt](/requirements.txt).

---

## Installation

You must have [python 3](https://www.python.org/) installed to run this application.

Firstly, clone the repository (alternatively you can download and extract the repo)

```
git clone https://github.com/Aritra587/calendrier.git
```

Then, change directories into the newly cloned repository.

```
cd calendrier
```

Then, using [pip](https://pip.pypa.io/en/stable/), install the application dependencies:

```
pip install -r requirements.txt
```

---

## Usage

You can run the application by:
```
python main.py [-h] [-v] [-e] [-c] [-d] [-ed] [-p] [-cp] [year] [month] [day]
```

To change the table format, visit the [tabulate github page](https://github.com/astanin/python-tabulate), choose one of the table formats and change the table_format preference to that value using the -cp flag.

For further help running the application:

```
python project.py --help
```

---

## File Structure Description

```
.
├─ constants.py -> constants
├─ helpers.py -> helper functions
├─ main.py -> run app
├─ events.csv -> events
├─ requirements.txt -> dependencies
├─ settings.ini -> settings (preferences)
├─ README.md -> instructions
└─ images -> images (primarily for README)
   ├─ calendar.png
   └─ demoThumbnail.jpg
```
