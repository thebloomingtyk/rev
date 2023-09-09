from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from account.manager import *
from django.core.validators import RegexValidator

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    SELLER = 2
    BUYER = 3

    ROLE_CHOICES = (
        (BUYER, 'BUYER'),
        (SELLER, 'SELLER'),
        (ADMIN, 'ADMIN'),
    )

    # for gender
    MALE = 1
    FEMALE = 2

    GENDER_CHOICES = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=False, null=False)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, blank=False, null=False, default=1)
    title = models.CharField(
        max_length=30, blank=True, verbose_name='title', null=True)
    email = models.EmailField(
        max_length=40, verbose_name='Email Address', unique=True, db_index=True)
    first_name = models.CharField(
        max_length=30, blank=True, verbose_name='First Name')
    middle_name = models.CharField(
        max_length=30, blank=True, default=None, null=True, verbose_name='Middle Name')
    last_name = models.CharField(
        max_length=30, blank=True, verbose_name='Last Name')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], max_length=17, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    login_attempt = models.IntegerField(default=0)

    objects = UserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'title']

    USERNAME_FIELD = 'email'

    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_first_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    class Meta:
        verbose_name_plural = "Users"
