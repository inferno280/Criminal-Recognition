import cv2
import face_recognition
import time

from twilio.rest import Client


def message(to_phone_number, message_body):
    # Your Twilio Account SID and Auth Token (replace with your own)
    account_sid = 'AC6526169694086340cf325f01418e0583'
    auth_token = '4d8362b0de847a3145dd6d53a7b52dc3'

# Create a Twilio client
    client = Client(account_sid, auth_token)

# Replace the following values with your own
    from_phone_number = '+14123654034'

# Message to send

    try:
        # Send the SMS
        message = client.messages.create(
            body=message_body,
            from_=from_phone_number,
            to=to_phone_number)

    # Print a confirmation message
        print(f"Message sent with SID: {message.sid}")

    except Exception as e:
        # Handle any errors
        print(f"Error: {str(e)}")

