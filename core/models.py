from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
                                        PermissionsMixin
from django.conf import settings
import uuid
import os


def generate_file_path(instance, original_name):
    extension = original_name.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('images/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Archive(models.Model):
    name = models.CharField(max_length=50)
    info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    info = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=generate_file_path)
    predicted_class = models.CharField(max_length=10, null=True)
    predicted_value = models.FloatField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archive = models.ForeignKey(
            Archive,
            on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
