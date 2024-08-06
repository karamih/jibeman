import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

service_account_file = 'config/jibeman-49521-346c9f679823.json'
fcm_url = 'https://fcm.googleapis.com/v1/projects/jibeman-49521/messages:send'


def send_fcm_notification(token, title, body):
    message_payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    auth_request = Request()
    credentials.refresh(auth_request)
    access_token = credentials.token

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8"
    }

    response = requests.post(fcm_url, headers=headers, data=json.dumps(message_payload))
    return response.status_code, response.json()
