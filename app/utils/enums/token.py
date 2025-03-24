from enum import Enum


class TokenType(Enum):
    EMAIL_CONFIRMATION = "email_confirmation"
    PHONE_NUMBER_CONFIRMATION = "phone_number_confirmation"
    PASSWORD_RESET = "password_reset"
    PASSWORD_CHANGE = "password_change"
