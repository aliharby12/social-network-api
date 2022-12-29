from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError("Users must have email address")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Gender_Types(models.TextChoices):
    MALE = "M", "M"
    FEMALE = "F", "F"


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    uuid = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(
        max_length=5, choices=Gender_Types.choices, null=True, blank=True
    )
    signed_up_holiday = models.CharField(max_length=256, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_gender_valid",
                check=models.Q(gender__in=Gender_Types.values),
            ),
        ]

    def __str__(self) -> str:
        return self.email
