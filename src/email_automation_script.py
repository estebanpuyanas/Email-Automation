import subprocess
import datetime

def get_next_monday():
    today = datetime.date.today()
    days_ahead = (7 - today.weekday()) % 7  # Days until next Monday
    next_monday = today + datetime.timedelta(days=days_ahead or 7)
    return next_monday.strftime("%m/%d/%Y")

def generate_email_content(name, company, position):
    with open("email_template.rtf", "r") as file:
        template = file.read()
    return template.format(name=name, company=company, position=position)

def schedule_email(recipient_name, recipient_email, company, position):
    email_body = generate_email_content(recipient_name, company, position)

    apple_script = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"Interest in {position} at {company}", content:"{email_body}", visible:true}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{recipient_email}"}}
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

        repeat = input("Do you want to send another email? (y/n): ").strip().lower()
        if repeat != 'yes':
            print("Program terminated.")
            break

if __name__ == "__main__":
    main()
