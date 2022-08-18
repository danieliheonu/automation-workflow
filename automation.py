from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from typing import List
import schedule
import time

# ask user for the type of trigger element they want to use
print("What type of trigger element do you want to use?")
print("1. Opt-in Trigger")
print("2. Time Trigger")
trigger_type = input("Enter 1 or 2: ")

# function that handles sending of emails
def send_email(subject: str, body: str, to: str):

    # initialize email message
    message = MIMEMultipart()
    message['subject'] = subject
    message.attach(MIMEText(body))

    #setup email server for mailtrap
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as smtp:
        smtp.login("b89c639e8c1d88", "f2178b1a6eab41")
        smtp.sendmail(from_addr="no-reply <no-reply@gmail.com>", to_addrs=to, msg=message.as_string())
        print("Email sent!")


# function that handles the opt-in trigger
def send_opt_in_email():

    print("Fill in the necessary information to sign up")
    name = input('Enter Name: ')
    email = input('Enter Email: ')

    # create email body
    body = f"Hi {name},\n\nYou have been added to our mailing list.\n\nThank you for subscribing!"
    # send email to each recipient
    send_email("You have been added to our mailing list!", body, email)

# function that handles the time trigger
def send_time_email():

    print("What time do you want to send the email? (HH:MM) in 24 hour format")
    name = input('Enter Name: ')
    email= input('List of subscriber emails to add (separated by space): ')
    _time = input('24 hour time (HH:MM): ')

    # create email body
    body = f"Hi {name},\n\nYou have been added to our mailing list.\n\nThank you for subscribing!"

    # create a schedule job to send email at the specified time
    def email_job():
        send_email("You have been added to our mailing list!", body, email)
        return schedule.CancelJob
    
    schedule.every().day.at(_time).do(email_job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    if trigger_type == "1":
        send_opt_in_email()
    elif trigger_type == "2":
        send_time_email()
    else:
        print("Invalid input")
        exit()