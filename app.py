from flask import Flask, Response, render_template
import random
from twilio.rest import Client



app= Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')
client = Client(app.config["TWILIO_SID"], app.config["TWILIO_TOKEN"])




@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')


@app.route("/compliments")
def list_compliments():
  handle = open(app.config['COMPLIMENT_LOCATION'])
  compliments = [x.strip() for x in handle.readlines()]
  return render_template('all_compliments.html', compliments=compliments)

@app.route("/compliment_phone")
def compliment():
  handle = open(app.config['COMPLIMENT_LOCATION'])
  compliments = [x.strip() for x in handle.readlines()]
  compliment = str(random.choice(compliments))
  xml = render_template("phone.xml", compliment=compliment)
  return Response(xml, mimetype="text/xml")

@app.route("/compliment_sms")
def compliment():
  handle = open(app.config['COMPLIMENT_LOCATION'])
  compliments = [x.strip() for x in handle.readlines()]
  compliment = str(random.choice(compliments))
  xml = render_template("sms.xml", compliment=compliment)
  return Response(xml, mimetype="text/xml")

@app.route('/send_sms_compliment')
def send_compliment():
  call = client.api.account.calls.create(
      to=app.config["TO_NUMBER"],
      from_=app.config["FROM_NUMBER"],
      url=app.config["TWIML_SMS_URL"])

  return call.sid
@app.route('/send_phone_compliment')
def send_compliment():
  call = client.api.account.calls.create(
      to=app.config["TO_NUMBER"],
      from_=app.config["FROM_NUMBER"],
      url=app.config["TWIML_PHONE_URL"])

  return call.sid
