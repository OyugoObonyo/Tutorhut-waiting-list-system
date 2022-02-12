from smtplib import SMTPRecipientsRefused
from flask import Flask, flash, redirect, render_template, request, url_for
from config import Config
import requests
import datetime
from flask_mail import Mail, Message
from dotenv import load_dotenv
from threading import Thread


app = Flask(__name__)
load_dotenv('.env')
app.config.from_object(Config)
mail = Mail(app)


@app.route('/')
def index():
    """
    Renders the application's home page
    """
    return render_template('index.html')


def update_sheets(user_email):
    """
    Function email as arguement and appends it to the emails spreadsheet
    """
    url = app.config["SHEETY_URL"]
    date_added = datetime.datetime.now().strftime("%d/%m/%y")
    headers = {
        "Authorization": app.config["SHEETY_TOKEN"]
    }
    row = {
            "email": {
                "addresses": user_email,
                "dateAdded": date_added
            }
        }
    check_email = requests.get(f"{url}?filter[addresses]={user_email}", headers=headers)
    if (len(check_email.json()['emails'])) > 0:
        return 1
    response = requests.post(url=url, json=row, headers=headers)
    return 0


def send_async_mail(app, message):
    """
    Make the email sending process asynchronous
    """
    with app.app_context():
        mail.send(message)


def send_email(subject, sender, recipient, body):
    """
    A function that sends a message confirming subscription to waitlist
    @subject: The email's subject
    @sender: The sender's email
    @recipient: The email of user signing up on waitlist
    @body: The email's body.
    """
    msg = Message(subject=subject, sender=sender, recipients=recipient)
    msg.html = body
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr


@app.route('/join-list', methods=['GET', 'POST'])
def join_list():
    """
    Method that appends users to the waiting list
    Users get an email confirming their registration after being added to list
    """
    email = request.form.get('email')
    if email != "":
        status = update_sheets(email)
        if status == 1:
            flash("You are already subscribed to our waiting list", "info")
            return redirect(url_for('index'))
        else:
            flash('You have succesfully subscribed to our waiting list', 'success')
            try:
                send_email(
                    subject="Tutorhut waiting list subscription",
                    sender=app.config['MAIL_USERNAME'],
                    recipient=[email],
                    body=render_template('email/email.html')
                )
            except SMTPRecipientsRefused:
                flash("Please enter a valid email address with a 'example@mail.com' format", "danger")
                return redirect(url_for('index'))
            finally:
                return redirect(url_for('index'))
    flash("email cannot be empty", "danger")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
