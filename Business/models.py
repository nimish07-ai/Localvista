from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from Account_App.models import BusinessAccount
User = get_user_model()  # Get the user model

class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=100)  # A title or description for the image
    image = models.ImageField(upload_to='images/')  # The field for storing the image file

    def __str__(self):
        return self.title



class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]  # Rating choices from 0 to 5

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField()
    user_account = models.ForeignKey(User, on_delete=models.CASCADE)
    business_account = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)

    def __str__(self):
        return f"Review by {self.user_account} for {self.business_account}"
