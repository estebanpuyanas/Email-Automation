#!/usr/bin/env python3

import subprocess
import datetime
import os 

TEMPLATE_PATH = os.path.expanduser("~/Desktop/projects/Email-Automation/email-template.txt")

def get_next_monday():
    today = datetime.date.today()
    days_ahead = (7 - today.weekday()) % 7  # Days until next Monday
    next_monday = today + datetime.timedelta(days=days_ahead or 7)
    return next_monday.strftime("%m/%d/%Y")

def generate_email_content(name, company, position):
    with open(TEMPLATE_PATH, "r") as file:
        template = file.read()
    # Fill placeholders in HTML template
    template = template.replace("{recipient_name}", name)
    template = template.replace("{company}", company)
    template = template.replace("{position}", position)
    return template

def schedule_email(recipient_name, recipient_email, company, position):
    email_body = generate_email_content(recipient_name, company, position)

    # Escape quotes and special characters for AppleScript
    email_body = email_body.replace('"', '\\"').replace("\n", "\\n")

    sender_email  = "puyanasalazar.e@northeastern.edu"
    mail_account = "Northeastern University"

    apple_script = f'''
    tell application "Mail"
        set theSender to "{sender_email}"
        set newMessage to make new outgoing message with properties {{subject:"Interest in {position} at {company}", content:"{email_body}", visible:true}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{recipient_email}"}}
            set sender to theSender
        end tell
    end tell

    tell application "System Events"
        tell process "Mail"
            set frontmost to true
            tell window "Interest in {position} at {company}"
                click pop up button "Signature:"
                delay 0.5
                click menu item "Northeastern" of menu of pop up button "Signature:"
            end tell
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
