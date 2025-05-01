#!/usr/bin/env python3

import subprocess
import datetime
import os
import re
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TEMPLATE_PATH = os.path.expanduser("~/Desktop/projects/Email-Automation/email-template.txt")

def get_next_monday():
    today = datetime.date.today()
    days_ahead = (7 - today.weekday()) % 7
    next_monday = today + datetime.timedelta(days=days_ahead or 7)
    return next_monday

def generate_email_content(name, company, position):
    with open(TEMPLATE_PATH, "r") as file:
        template = file.read()
    template = template.replace("{recipient_name}", name)
    template = template.replace("{company}", company)
    template = template.replace("{position}", position)
    return template

def schedule_email(recipient_name, recipient_email, company, position):
    email_body = generate_email_content(recipient_name, company, position)\
                    .replace('"', '\\"')\
                    .replace("\n", "\\n")

    sender_email = "puyanasalazar.e@northeastern.edu"

    # split date into month, day, year
    next_monday = get_next_monday()
    month = next_monday.strftime("%-m")
    day   = next_monday.strftime("%-d")
    year  = next_monday.strftime("%Y")

    # fixed time at 8:00 AM, split into hour, minute, AM/PM
    hour   = "8"
    minute = "00"
    ampm   = "AM"

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
            
            -- Ensure the message window is active
            set targetWindow to front window
            
            -- Set the signature
            tell targetWindow
                click pop up button "Signature:"
                delay 0.5
                click menu item "Northeastern" of menu of pop up button "Signature:"
                delay 1
            end tell

            -- Navigate through the UI to find the "Send Later" button
            set toolbarView to first toolbar of targetWindow
            set toolbarItemViewer to first group of toolbarView
            set sendGroup to last group of toolbarItemViewer
            
            -- Find and click the schedule button (last menu button in the send group)
            set scheduleButton to last menu button of sendGroup
            click scheduleButton
            delay 0.5
            
            -- Select "Send Later..." from the dropdown menu
            try
                click menu item "Send Later..." of menu 1 of scheduleButton
            on error
                try
                    click menu item "Send Later…" of menu 1 of scheduleButton
                on error
                    try
                        set laterItem to (first menu item of menu 1 of scheduleButton whose name contains "Send Later")
                        click laterItem
                    on error
                        display dialog "Could not find 'Send Later...' option. Please check the script." buttons {{"OK"}} default button "OK"
                    end try
                end try
            end try

            -- —— NEW: break date+time into cells ——
            delay 0.5
            keystroke "{month}"
            keystroke tab
            keystroke "{day}"
            keystroke tab
            keystroke "{year}"
            
            keystroke tab
            keystroke "{hour}"
            keystroke tab
            keystroke "{minute}"
            keystroke tab
            keystroke "{ampm}"
            
            delay 0.3
            click button "Schedule" of sheet 1 of front window
        end tell
    end tell
    '''

    subprocess.run(["osascript", "-e", apple_script])

def is_valid_email(email):
    # Basic regex for email format (contains @ and a dot in the domain)
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(pattern, email)

def prompt_input(prompt_message, validation_func=None):
    while True:
        value = input(prompt_message).strip()
        if not value:
            logging.error("Input cannot be blank. Please try again.")
            continue
        if validation_func and not validation_func(value):
            logging.error("Invalid format. Please try again.")
            continue
        return value

def main():
    while True:
        recipient_name = prompt_input("Enter recipient's name: ")
        recipient_email = prompt_input("Enter recipient's email: ", is_valid_email)
        company = prompt_input("Enter company name: ")
        position = prompt_input("Enter position title: ")

        try:
            schedule_email(recipient_name, recipient_email, company, position)
            msg = f"Email to {recipient_name} at {recipient_email} scheduled for next Monday at 8 AM."
            logging.info(msg)
            print(msg)
        except Exception as e:
            logging.error(f"An error occurred while scheduling the email: {e}")

        while True:
            repeat = input("Do you want to schedule another email? (y/n): ").strip().lower()
            if repeat == "y":
                break
            elif repeat == "n":
                logging.info("Exiting...")
                print("Exiting...")
                return
            else:
                logging.error("Invalid input. Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()
    