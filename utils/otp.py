import random
from ippanel import Client
from django.core.exceptions import ValidationError

from client_auth.models import TOTPModel


def generate_and_send_totp(phone_number):
    totp_code = f"{random.randint(100000, 999999)}"

    totp = TOTPModel(phone_number=phone_number, otp=totp_code)
    try:
        totp.full_clean()
        totp.save()
        send_sms(phone_number, totp_code)
        return True
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return False


def send_sms(phone_number, totp_code):
    api_key = 'U1XDtYsrczPs6DNPyuBVCrMIe2iAA9b5L9Mel8JIrHQ='
    sms = Client(api_key)

    pattern_values = {
        "verification-code": totp_code,
    }
    try:
        sms.send_pattern(
            "eskdg5s6vd5f70a",
            "+983000505",
            phone_number,
            pattern_values,
        )
    except Exception as e:
        print(f"SMS Error: {e}")
