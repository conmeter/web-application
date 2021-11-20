import random
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from PIL import Image


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, is_moderator, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_verified=False,
            is_superuser=is_superuser,
            is_moderator=is_moderator,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, verbose_name="Enter your email address")
    name = models.CharField(max_length=254, null=False, blank=False, verbose_name="Enter your name")
    image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    is_moderator = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=False, unique=True, null=False)
    dob = models.DateField(null=False, blank=False, verbose_name="Enter you date of birth", help_text="YYYY-MM-DD")
    t_c = models.BooleanField(null=False, blank=False, default=False,
                              verbose_name="Please accept the terms and conditions")

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['dob', 'phone']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        # if(self.image):
        #     img = Image.open(self.image.name)

        #     if img.height > 300 or img.width > 300:
        #         output_size = (300, 300)
        #         img.thumbnail(output_size)
        #         img.save(self.image.name)


class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    user_email = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post_id = models.ForeignKey("posts.Posts", on_delete=models.CASCADE, null=True, blank=True)
    issue_head = models.CharField(max_length=1024, null=False, blank=False, verbose_name="ISSUE")
    issue_body = models.TextField(null=False, blank=False, verbose_name="DESCRIPTION")

    def __str__(self):
        return self.issue_head


class OTPManager(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    key = models.CharField(max_length=1024, null=False, blank=False)
