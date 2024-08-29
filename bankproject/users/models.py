from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    postcode = models.CharField(max_length=10, blank=True, null=True)
    business_postcode = models.CharField(max_length=10, blank=True, null=True)
    customer_number = models.CharField(max_length=10, unique=True)
    pin = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.user.username}'s Profile"
