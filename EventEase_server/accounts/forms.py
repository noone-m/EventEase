from django.contrib.admin.forms import AdminAuthenticationForm
from django.forms import ValidationError


class CustomAuthForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_superuser:
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
            )