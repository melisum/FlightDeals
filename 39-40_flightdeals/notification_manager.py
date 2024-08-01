import os
from twilio.rest import Client

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):

        self.client = Client(account_sid, auth_token)

    def send_message(self, message_details):

        self.message = self.client.messages.create(
            body=message_details,
            from_='+19136751124',
            to='+420735193925'
        )
        print(self.message.status)