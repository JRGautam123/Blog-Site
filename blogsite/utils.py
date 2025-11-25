import uuid
import random
from django.utils import timezone
import threading
from django.db import close_old_connections


# token generation
def generate_verification_token():
    """Generate a unique UUID token."""
    return uuid.uuid4()

#otp generation
def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

class EmailThread(threading.Thread):
    def __init__(self, msg, user=None):
        self.msg = msg
        self.user = user
        super().__init__()

    def run(self):
        close_old_connections()
        try:
            self.msg.send()

        except:
            if self.user:
                try:
                    close_old_connections()
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user = User.objects.get(pk=self.user.pk)
                    user.is_email_send_fail = True
                    user.save()
                except Exception as db_error:
                    print(db_error)
        finally:
            close_old_connections()

