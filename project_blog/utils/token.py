from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp = 1000):
        return (
            str(user.is_active) + str(user.pk) + str(timestamp)
        )

token_generator = AccountActivationTokenGenerator()