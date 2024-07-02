from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.authtoken.models import Token
from services.models import Service

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, phone, email, password, **extra_fields):
        """
        Create and save a user with the given name,phone, email, and password.
        """
        email = self.normalize_email(email)

        user = self.model(first_name=first_name, last_name=last_name, email=email,phone = phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_service_provider", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(first_name, last_name, phone, email, password, **extra_fields)

    def create_service_provider(self, first_name, last_name, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_service_provider", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(first_name, last_name, phone, email, password, **extra_fields)
    
    def create_superuser(self, first_name, last_name, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_service_provider", False)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(first_name, last_name, phone, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=150, null = False)
    last_name = models.CharField(_("last name"), max_length=150, null = False)
    email = models.EmailField(_("email address"), null = False, unique = True)
    phone = models.CharField(_("phone number"), max_length = 20, null = False)
    is_service_provider = models.BooleanField(
        _("service provider status"),
        default=False,
        help_text=_("Designates whether the user has service or not."),
    )
    is_superuser = models.BooleanField(
        _("super user status"),
        default=False,
        help_text=_("Designates whether the user is super user or not."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","phone","password"]


class OTP(models.Model):
    user =models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = True,
    )
    service =models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null = True,
    )
    code = models.CharField(max_length = 6, null = False)
    expire_date = models.DateTimeField()
    is_verified = models.BooleanField(default =False)

    def save(self, *args, **kwargs):
        self.expire_date = timezone.now() + timedelta(seconds = 60)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expire_date
        
    def __str__(self):
        return f'{self.user.email} - {self.code}'
   
        
class PasswordChangeRequested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)
    is_requested = models.BooleanField(default = False)


class EmailVerified(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensures each user has one unique email verification record
    is_verified = models.BooleanField(default=False)  # Field to store verification status
    verification_date = models.DateTimeField(auto_now_add = True,null=True)  # Optional field to store the date of verification
    verfication_token = models.CharField(max_length=100, unique=True)  # Unique code for verification
    expire_date = models.DateTimeField(now)
    
    def save(self, *args, **kwargs):
        self.expire_date = timezone.now() + timedelta(seconds = 60)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expire_date
    
    def __str__(self):
        return f"{self.user.username} - Verified: {self.is_verified}"