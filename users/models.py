from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

# Create your models here.
ROLES = [("developer", "developer")]


class MyAccountManager (BaseUserManager):
    def create_user(self, email, username, role, password=None):
        if not email:
            raise ValueError("users must have an email address")
        if not username:
            raise ValueError("users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, username, role, password):
        user = self.create_user(email=self.normalize_email(email),
                                password=password,
                                username=username,
                                role=role,
                                )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class Account(AbstractBaseUser):
    ROLES = [
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        ('Facility Manager', 'Facility Manager')
    ]
    email = models.EmailField(verbose_name="email",
                              max_length=254, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now=False, auto_now_add=True)
    last_joined = models.DateTimeField(
        verbose_name="last joined", auto_now=True, auto_now_add=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # custom fields
    role = models.CharField(max_length=50, choices=ROLES, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'role']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obk=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


#
class Customer(models.Model):
    # username
    # firstname
    # lastname
    # emailaddress
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    role = models.CharField(max_length=50, choices=ROLES)
    points = models.FloatField()

    def __str__(self):
        return self.user.username



class Admin(models.Model):
    # username
    # firstname
    # lastname
    # emailaddress
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    role = models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        return self.user.username + " : " + self.user.email



class FacilityResponsible(models.Model):
    # username
    # firstname
    # lastname
    # emailaddress
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    role = models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        return self.user.username + " : " + self.user.email
