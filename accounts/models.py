from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class CustomUserManager(BaseUserManager):
#     """
#     Used for updating default create user behaviour
#     """
#     def create_user(self, phone_no, password, **kwargs):
#         # implement create user logic
#         user = self.model(phone_no=phone_no, **kwargs)
#         user.set_password(password)
#         user.save()
#         return user
    
#     def create_superuser(self, phone_no, password, **kwargs):
#         # creates superuser.
#         self.create_user(phone_no, password)

# class CustomUser(AbstractUser):
#     username = None
#     phone_no = models.CharField(unique=True, max_length=20)
#     city = models.CharField(max_length=40)
#     USERNAME_FIELD = "phone_no"
#     objects = CustomUserManager()


class UserProfile(models.Model):
    user = models.OneToOneField('auth.user', related_name='user_profile', on_delete=models.CASCADE)
    phone_no = models.CharField(unique=True, max_length=40)
    city = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username