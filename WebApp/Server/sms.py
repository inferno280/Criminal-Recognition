import cv2
import face_recognition
import time

from twilio.rest import Client


def message(to_phone_number, message_body):
    # Your Twilio Account SID and Auth Token (replace with your own)
    account_sid = 'AC11b8477760824169d34cc8ef5e939062'
    auth_token = 'a969ce1c3953ba4bc03789aab9ef2482'

# Create a Twilio client
    print("Hello")
    client = Client(account_sid, auth_token)

# Replace the following values with your own
    from_phone_number = '+15416528460'

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

