from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, myuser, timestamp):
        return (
            six.text_type(myuser.pk) + six.text_type(timestamp) + six.text_type(myuser.username)
        )

account_activation_token = AccountActivationTokenGenerator