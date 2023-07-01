from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):

    """
    A class that generates a token for activating a user account.

    This class inherits from Django's built-in `PasswordResetTokenGenerator` class and
    generates a hash value using the user's primary key, timestamp, and user's active status.

    Attributes:
        None

    Methods:
        _make_hash_value(user, timestamp):
            Returns a string hash value based on the user's primary key, timestamp, and
            active status.

    Usage:
        Instantiate an object of this class to generate a token for account activation. The
        `account_activation_token` variable is an instance of this class that can be used to
        generate a token.

    Example:
        account_activation_token = TokenGenerator()
        token = account_activation_token.make_token(user)
    """

    def _make_hash_value(self, user, timestamp):
        return(six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))
    

account_activation_token = TokenGenerator()

