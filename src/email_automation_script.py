#!/usr/bin/env python3

import subprocess
import datetime
import os 

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
    next_monday = get_next_monday()
    # split date into month, day, year
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
                        display dialog "Could not find 'Send Later...' option. Please check the script." buttons {"OK"} default button "OK"
                    end try
                end try
            end try

            -- —— NEW: break date+time into cells ——
            delay 0.5
            -- date: month → day → year
            keystroke "{month}"
            keystroke tab
            keystroke "{day}"
            keystroke tab
            keystroke "{year}"
            
            -- time: hour → minute → AM/PM
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
    