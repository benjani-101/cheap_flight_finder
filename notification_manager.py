from twilio.rest import Client
import os

class NotificationManager:
    def __init__(self):
        self.tw_client = Client(os.environ.get('TW_ACCOUNT_SID'), os.environ.get('TW_AUTH_TOKEN'))
    #This class is responsible for sending notifications with the deal flight details.
    def sms_message(self, message, to_number):
        message = self.tw_client.messages.create(
            body=message,
            from_=os.environ.get('TW_PHONE_NUMBER'),
            to=to_number
        )

        print(message.sid)
        print(message.status)