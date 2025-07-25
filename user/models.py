
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
    
USER_TYPE_CHOICES = [
    ('business', 'Business'),
    ('employee', 'Employee'),
]
class User(AbstractBaseUser, PermissionsMixin):
    def user_profile_pic_path(instance, filename):
        return f'profile_pics/user_{instance.id}/{filename}'

    USER_TYPE_CHOICES = [
        ('business', 'Business'),
        ('employee', 'Employee'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='employee')

    # New Fields
    education = models.CharField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    credit_score = models.IntegerField(blank=True, null=True, default=100)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)
