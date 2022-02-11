from flask import Flask, flash, redirect, render_template, url_for
from config import Config
import requests
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired
from wtforms import StringField, SubmitField


app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)


@app.route('/')
def index():
    """
    Renders the application's home page
    """
    return render_template('index.html')


def update_sheets(email):
    """
    Function email as arguement and appends it to the emails spreadsheet
    """
    # Remember to first loop through email list to confirm email is unique
    url = app.config['SHEETY_URL']
    headers = {
        "Authorization": app.config['SHEETY_TOKEN']
    }
    data = {
        "sheet1": {
            "EMAIL ADDRESSES": email
        }
    }
    response = requests.post(url=url, json=data, headers=headers)


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
    mail.send(msg)


class EmailSignUpForm(FlaskForm):
    """
    A class representing the sign up to waitlist form
    """
    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField('Get Early Access')


@app.route('/join-list')
def join_list():
    """
    Method that appends users to the waiting list
    Users get an email confirming their registration after being added to list
    """
    form = EmailSignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        update_sheets(email)
        # <<<<<<add a flash message in case user tries to re-register
        flash('You have succesfully subscribed to our waiting list', 'success')
        send_email(
            subject="Tutorhut waiting list subscription",
            sender=app.config['MAIL_USERNAME'],
            recipient=email,
            body=render_template('email/email.html')
        )
        return redirect(url_for('index'))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
