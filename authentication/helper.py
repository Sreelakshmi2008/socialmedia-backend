# helper.py

import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from dotenv import load_dotenv
print("TWILIO_ACCOUNT_SID before dotenv:", os.environ.get('TWILIO_ACCOUNT_SID'))


# Load dotenv
load_dotenv()

print("TWILIO_ACCOUNT_SID after dotenv:", os.environ.get('TWILIO_ACCOUNT_SID'))


print("TWILIO_AUTH_TOKEN:", os.environ.get('TWILIO_AUTH_TOKEN'))
print("TWILIO_VERIFY_SERVICE_SID:", os.environ.get('TWILIO_VERIFY_SERVICE_SID'))

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])


service = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])
print(service,"verifyyyyy")


# sendin otp to phone using twilio service
def send(phone):

    service.verifications.create(to=phone, channel='sms')
    print(phone)


# verifying code sent and code given by user
def check(phone, code):
    try:
        print(phone,code)
        # formatted_phone = f"+91{phone}"  # Assuming phone is a string without a leading '+'
        # print(f"Checking code: {code} for formatted phone: {formatted_phone}")
        result = service.verification_checks.create(to=phone, code=code)
        print(result,"k")
    except TwilioRestException as e:
        print(f"TwilioRestException: {e}")
        print(f"TwilioRestException Code: {e.code}")
        print(f"TwilioRestException Message: {e.msg}")
        
        return False
    return result.status == 'approved'