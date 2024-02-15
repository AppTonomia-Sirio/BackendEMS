from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class PasswordValidator(BaseValidator):
    message = 'Password is not valid'
    code = 'invalid'

    def __init__(self, password=None):
        super().__init__(password)

    def __call__(self, password):
        if password is not None:
            if len(password) < 4:
                raise ValidationError(self.message, code=self.code)
        else:
            raise ValidationError(self.message, code=self.code)
