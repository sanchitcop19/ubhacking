from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import requests
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from gmail import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/contacts']
# Use a service account
cred = credentials.Certificate('ubhacking-88c6108cedd9.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

first, second = None, None

app = Flask(__name__)
firestore_url = 'https://ubhacking.firebaseio.com/users/.json'

current_otp = None
first_email, second_email = None, None

store = {
    "mtb": "M&T Bank",
    "buffalo": "University at Buffalo",
    "gmail": "Google",
    "github": "GitHub",

}
'''
job_store = {
    "applied": [
        "Google",
        "Facebook",
        "Apple",
        "Twilio",
        "ValueCentric",
        "IBM"
    ],
    "offers": [
        "Microsoft"
    ],
    "rejected": [
        "AirBnb",
        "Uber",
        "Lyft"
    ]
}
'''

job_store = db.collection(u'job_store').document(u'1').get().to_dict()
@app.route('/add_friend')
def add_friend():
    global current_otp, first_email
    if "otp" in request.args:
        if request.args["otp"] == str(current_otp):
            current_otp = None
            second_email = request.args["email"]
            first_user = db.collection(u'users').document(first_email)
            second_user = db.collection(u'users').document(second_email)
            print(first_user, second_user)
            user1 = first_user.get().to_dict()
            user2 = second_user.get().to_dict()
            if user2['email'] not in user1['friends']:
                user1['friends'].append(user2['email'])
                user2['friends'].append(user1['email'])
            first_user.set(user1)
            second_user.set(user2)
            return render_template('success.html', facebook = user1['facebook'])
    elif "email" in request.args:
        current_otp = 467355
        first_email = request.args["email"]
        return render_template('add_friend.html', otp = current_otp)


    # two buttons: request OTP and enter OTP
    # let the user press a button that will give them a random 6 digit number which the other person can enter
    # save the fact that they are friends
    # save contact details through the people API
    return "<h1>add a friend</h1>"


@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.args:
        user = {}
        doc_ref = db.collection(u'users').document(request.args["email"])

        for key, value in request.args.items():
            user[key] = value
        user["friends"] = []
        doc_ref.set(user)
        #response = requests.put(firestore_url, data = json.dumps(user))
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    job_store = db.collection(u'job_store').document(u'1').get().to_dict()
    return render_template('dashboard.html', applied = job_store["applied"][::-1], offers = job_store["offers"][::-1], rejected = job_store["rejected"][::-1])

@app.route('/update')
def update():
    from_, message = get_last_email()
    message = str(message)
    domain = re.search('@[a-z]+.(com|edu)', from_).group()
    domain = domain[1:domain.index('.')]
    domain = store[domain]
    # call ML model on message
    company = domain.capitalize() if domain.islower() else domain
    status = ""
    if "unfortunately" in message or "unable" in message:
        job_store["applied"].remove(company)
        status = "rejected"
    elif "congratulations" in message:
        job_store["applied"].remove(company)
        status = "offers"
    elif "has been received" in message:
        status = "applied"
    if not status:
        return redirect(url_for('dashboard'))
    if company in job_store[status]:
        return jsonify({})
    job_store[status].append(company)

    doc_ref = db.collection(u'job_store').document(u'1')
    doc_ref.set(job_store)
    return jsonify({company: message, "status": status})

if __name__ == '__main__':
    app.run(debug = True)
