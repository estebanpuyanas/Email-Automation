# Email-Automation

This is a simple Python Script I wrote to automate email writing, scheduling, and sending. I decided to do this to automate and simplify a crucial point of the job application process: sending networking emails to recruiters/managers/current employees in the companies I am applying to.

To run the program, first create a virtual enviornment by running the following command in the command line terminal:
`python3 -m venv .venv`

Afterwards, go over to the `email-automation.code-workspace` file, and depending which machine you're working on (either MacOS/Linux or Windows), comment out the line that is **not** your machine OS:

```
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python", // For macOS/Linux
"python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe", // For Windows
```

Additionally, since the script uses Apple's System Events application to simulate keystrokes to enable email scheduling, you will need to ensure that System Events has accessibility enabled, to do this go to `System Settings` and navigate to: `Privacy & Security > Accessibility` click on the `+` to grant a new entity access and then navigate to the `Macintosh HD` folder and then locate the System Events application by doing the following: `System > Library > CoreSerivces > System Events`, once you have granted access you should be good to go!

The script works in a very simple manner. It first finds the next Monday by using Python's `datetime` package. I do this because I like to schedule networking emails to be sent at Monday 8 AM, so when the receiver goes into the office, my email will be one of the first things they see in their inbox.

Afterwards, the function `generate_email_content` accesses a `.rtf` file with the email template, it has `{name}, {company}, {position}` placeholders were I enter the name of the recruiter, company, and position I am applying to and fills them in to generate the email.

The `schedule_email` function then leverages AppleScript to generate the email inside the MacOS email app and send it. I chose to implement this feature like this because I have always used MailOS over downlaoding the providers (in this case Outlook) native application by integrating my email account in the settings, but it is not hard to instead use the email provider API to have the same functionality.

Lastly, the `main` method runs the program, asking the user to enter the information forthe placeholders needed for `generate_email_content` and asks the user to either send another email or quit the program.
