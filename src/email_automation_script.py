#!/usr/bin/env python3

import subprocess
import datetime
import os 

TEMPLATE_PATH = os.path.expanduser("~/Desktop/projects/Email-Automation/email_template.html")

def get_next_monday():
    today = datetime.date.today()
    days_ahead = (7 - today.weekday()) % 7  # Days until next Monday
    next_monday = today + datetime.timedelta(days=days_ahead or 7)
    return next_monday.strftime("%m/%d/%Y")

def generate_email_content(name, company, position):
    with open(TEMPLATE_PATH, "r") as file:
        template = file.read()
    # Fill placeholders in HTML template
    return template.format(name=name, company=company, position=position)

def schedule_email(recipient_name, recipient_email, company, position):
    email_body = generate_email_content(recipient_name, company, position)

    # Escape quotes and special characters for AppleScript
    email_body = email_body.replace('"', '\\"').replace("\n", "\\n")

    apple_script = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"Interest in {position} at {company}", content:"{email_body}", visible:true}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{recipient_email}"}}
            set content type to "text/html"
            set send date to date "{get_next_monday()} 08:00:00 AM"
            send
        end tell
    end tell
    '''

    subprocess.run(["osascript", "-e", apple_script])

def main():

    while True:
        recipient_name = input("Enter recipient's name: ")
        recipient_email = input("Enter recipient's email: ")
        company = input("Enter company name: ")
        position = input("Enter position title: ")

        schedule_email(recipient_name, recipient_email, company, position)
        print(f"Email to {recipient_name} at {recipient_email} scheduled for next Monday at 8 AM.")

        repeat = input("Do you want to schedule another email? (y/n): ").strip().lower()
        if repeat != 'y':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
