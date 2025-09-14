from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone


def validate_age_18_plus(value):
    if value:
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise ValidationError('Возраст должен быть не менее 18 лет')


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField('Имя', max_length=50)
    middle_name = models.CharField('Отчество', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=50)
    birth_date = models.DateField('Дата рождения', null=True, validators=[validate_age_18_plus])
    avatar = models.ImageField('Аватар', upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    confirmation_expires = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date']

    is_active = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    confirmation_expires = models.DateTimeField(blank=True, null=True)

    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()