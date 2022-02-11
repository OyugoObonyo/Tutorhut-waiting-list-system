from flask import Flask, render_template, request
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


def update_sheets():
    """
    Documentation
    """
    pass


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


if __name__ == "__main__":
    app.run(debug=True)
