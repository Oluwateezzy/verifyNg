from twilio.rest import Client
from app.core.config import settings

client = Client(settings.twilio_account_sid, settings.twilio_auth_token)


def send_otp(phone_number: str, otp_code: str):
    """Send a One-Time Password (OTP) to the user's phone."""
    message = client.messages.create(
        body=f"Your OTP is {otp_code}",
        from_=settings.twilio_phone_number,
        to=phone_number,
    )
    return message.sid
    # verification = client.verify.v2.services(
    #     settings.twilio_account_sid
    # ).verifications.create(to=phone_number, channel="sms")
    # return verification.status


def verify_otp(phone_number: str, otp_code: str):
    """Verify the OTP entered by the user."""
    verification_check = client.verify.v2.services(
        settings.twilio_account_sid
    ).verification_checks.create(to=phone_number, code=otp_code)
    return verification_check.status
