from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    # Arbitrary fields as a mockup
    
    address = models.TextField(name='User address', max_length=200, blank=True)
    phone = models.CharField(name='Phone number', max_length=14, blank=True)   # TODO: phone number validation
    
