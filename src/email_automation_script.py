#!/usr/bin/env python3

import subprocess
import datetime
import os 

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "email_template.rtf")

def get_next_monday():
    today = datetime.date.today()
    days_ahead = (7 - today.weekday()) % 7  # Days until next Monday
    next_monday = today + datetime.timedelta(days=days_ahead or 7)
    return next_monday.strftime("%m/%d/%Y")

def generate_email_content(name, company, position):
    with open(TEMPLATE_PATH, "r") as file:
        template = file.read()
    return template.format(name=name, company=company, position=position)

def schedule_email(recipient_name, recipient_email, company, position):
    email_body = generate_email_content(recipient_name, company, position)
    next_monday = get_next_monday()

    apple_script = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"Interest in {position} at {company}", content:"{email_body}", visible:true}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{recipient_email}"}}
            activate
            delay 1
            tell application "System Events"
                keystroke "d" using {{command down}}
                delay 1
                key code 125 -- arrow down to select "Send Later"
                delay 0.5
                key code 36 -- press enter
                delay 0.5
                keystroke "{next_monday}"
                key code 48 -- tab to time field
                keystroke "08:00AM"
                key code 36 -- press enter to confirm
            end tell
        end tell
    end tell
    '''

    subprocess.run(["osascript", "-e", apple_script])

def main():
    recipient_name = input("Enter recipient's name: ")
    recipient_email = input("Enter recipient's email: ")
    company = input("Enter company name: ")
    position = input("Enter position title: ")

    schedule_email(recipient_name, recipient_email, company, position)
    print(f"Email to {recipient_name} at {recipient_email} scheduled for next Monday at 8 AM.")

if __name__ == "__main__":
    main()
