from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError("Username did'nt come")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise TypeError("Password didn't come")
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=50, null=True)
    avatar = models.ImageField(upload_to='profile/', null=True, blank=True)
    bio = models.TextField()
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_active = models.BooleanField(default=False, verbose_name='Active user'),
    is_staff = models.BooleanField(default=False, verbose_name='Staff user'),
    date_login = models.DateTimeField(auto_now=True, verbose_name='Last Login'),
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')

    object = AccountManager
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email',
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.email}"

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data


#
# @receiver(post_save, sender=User)
# def user_post_save(instance, sender, created, *args, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_profile(instance, sender, *args, **kwargs):
#     instance.profile.save()

