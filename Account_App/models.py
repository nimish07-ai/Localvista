from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from Business.models import Cuisine,Review

class User(models.Model):
    # Fields specific to user accounts
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='user_images/')
    is_vegetarian = models.BooleanField()

class BusinessAccount(models.Model):
    # Other fields...
    business_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    cuisines = models.ManyToManyField(Cuisine)  # Many-to-Many field for cuisines
    location = models.PointField(geography=True, null=True, blank=True)  # Geolocation
    reviews = models.ManyToManyField(Review, related_name='business_accounts')
    images = models.ManyToManyField(Image)
    menu= models.ManyToManyField(Image)

class Account(AbstractUser):
    # Add common fields for all account types here
    is_user = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)

    # Connect each Account to its associated User or BusinessAccount
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    business_profile = models.OneToOneField(BusinessAccount, on_delete=models.CASCADE, null=True, blank=True)



