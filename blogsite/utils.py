import uuid
import random
from django.utils import timezone


# token generation
def generate_verification_token():
    """Generate a unique UUID token."""
    return uuid.uuid4()

#otp generation
def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))
