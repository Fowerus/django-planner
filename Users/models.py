from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model



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
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update_at')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ('surname', 'first_name', 'second_name')

    objects = UserManager()

    def __str__(self):
        return f'id: {self.id} | email: {self.email} | phone: {self.phone}'

    def get_short_name(self):
        return f'{self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']


class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    prefix = models.SlugField(max_length=50, unique=True, blank=True, verbose_name='Prefix')
    lead = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
                             related_name='user_team_lead', verbose_name='Lead')
    users = models.ManyToManyField(get_user_model(), related_name='user_team_users',
                                   verbose_name='Users')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update_at')

    def __str__(self):
        return f'id: {self.id} | prefix: {self.prefix} | ' \
               f'lead: {self.lead.first_name} {self.lead.surname[0]}.'

    def save(self, *args, **kwargs):
        if len(self.name.split()) > 1:
            self.prefix = self.name.title().replace(' ', '')
        else:
            self.prefix = self.name

        return super(Team, self).save(args, kwargs)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['-created_at']


class Proposal(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
        related_name='project_proposal_team', verbose_name='Team')
    project = models.ForeignKey('Projects.Project', on_delete=models.CASCADE,
        related_name='project_proposal_project', verbose_name='Project')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update_at')

    def __str__(self):
        return f'id: {self.id} | team: {self.team.id} | ' \
               f'project: {self.project.id}'


    class Meta:
        verbose_name='Proposal'
        verbose_name_plural='Proposals'
        ordering=['-created_at']
