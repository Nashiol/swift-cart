# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings


# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('CUSTOMER', 'customer'),
        ('VENDOR', 'vendor'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, null=True)

    username = models.CharField(max_length=200, blank=True, unique=True)
    email = models.EmailField(max_length=200, blank=True, unique=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email

    



class AccountReview(models.Model):
    user_email = models.EmailField() 
    review_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user_email} on {self.submitted_at}"


class Customer_Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name='customer_profile')
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Vendor_Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name='vendor_profile')
    name = models.CharField(max_length=200, null=False, blank=False)
    phone_number = models.CharField(max_length=200, null=False, blank=False)
    email = models.CharField(max_length=200, null=False, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profiles_photos/')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True)
    business_name = models.CharField(max_length=200, null=True, blank=True, unique=False)
    city = models.CharField(max_length=100, null=True, blank=True, unique=False)
    business_description = models.TextField(null=True, blank=True)
   

    def __str__(self):
        return str(self.name)


