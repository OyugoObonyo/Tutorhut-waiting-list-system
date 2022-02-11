from flask import Flask, flash, redirect, render_template, request, url_for
from config import Config
import requests


app = Flask(__name__)
app.config.from_object(Config)


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


def send_email(email):
    """
    A function that se
    """
    pass


@app.route('/join-list')
def join_list():
    """
    Method that appends users to the waiting list
    Users get an email confirming their registration after being added to list
    """
    # get email address from form
    email = request.form.get('email')
    # ensure email
    if email is None:
        return redirect(url_for('index'))
    update_sheets(email)
    # add a flash message in case user tries to re-register
    send_email(email)
    flash('You have succesfully subscribed to our waiting list', 'success')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
