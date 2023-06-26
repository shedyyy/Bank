from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from user.iban import generate_random_iban


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("User must have an email")

        user = self.model(
            email=email,
          
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None):
        """ """
        user = self.create_user(
          
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


roles = (
    ("client", "client"),
    ("staff", "staff"),
)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    username = models.CharField(max_length=255, default="Test")

    role = models.CharField(
        max_length=10, null=True, blank=True, choices=roles, default="client"
    )
    is_active = models.BooleanField(default=True)
    iban = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.iban:
            self.iban = generate_random_iban()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.username)

    def get_role(self):
        return self.role

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
