from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField



class UserManager(BaseUserManager):
    def _create_user(self, surname=None, first_name=None, second_name=None, email=None,
                     phone=None, password=None, **extra_fields):
        if email is not None:
            email = self.normalize_email(email)
        user = self.model(surname=surname, first_name=first_name,
                          second_name=second_name, email=email, phone=phone,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, surname=None, first_name=None, second_name=None, email=None,
                    phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(surname=surname, first_name=first_name,
                                 second_name=second_name, email=email,
                                 phone=phone, password=password, **extra_fields)

    def create_superuser(self, surname=None, first_name=None, second_name=None,
                         email=None, phone=None, password=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(surname=surname, first_name=first_name,
                                 second_name=second_name, email=email, phone=phone,
                                 password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    surname = models.CharField(max_length=50, verbose_name='Surname')
    first_name = models.CharField(max_length=50, verbose_name='First name')
    second_name = models.CharField(max_length=50, verbose_name='Second name')

    email = models.EmailField(max_length=60, unique=True, verbose_name='Email')
    phone = PhoneNumberField(unique=True, blank=True, null=True, verbose_name='Phone')

    avatar = models.ImageField(
        upload_to='users/', max_length=255, null=False, blank=False,
        verbose_name='Avatar', default='users/default-user-image.png')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')
    updated_at = models.DateTimeField(auto_now=False, verbose_name='Update_at')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ('surname', 'first_name', 'second_name')

    objects = UserManager()

    def __str__(self):
        return f'id: {self.id} | email: {self.email} | phone: {self.phone}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']


class Team:
    name = models.CharField(max_length=50, verbose_name='Name')
    lead = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='user_team_lead', verbose_name='Lead')
    users = models.ManyToManyField(User, related_name='user_team_users',
                                   verbose_name='Users')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')
    updated_at = models.DateTimeField(auto_now=False, verbose_name='Update_at')

    def __str__(self):
        return f'id: {self.id} | name: {self.name} | ' \
               f'name: {self.lead.name} + " {self.lead.surname}[0]"'

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['-created_at']
