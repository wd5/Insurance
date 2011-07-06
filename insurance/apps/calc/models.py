from django.db import models
from django.contrib.auth.models import User



class InsurancePolicy(models.Model):
    STATE_CHOICES = (
        ('init', 'Initializing'),
        ('process', 'Being worked on'),
        ('active', 'Active'),
        ('ended', 'Ended'),
    )
    PAYMENT_CHOICES = (
        ('payed', 'Fully payed'),
        ('unpayed', 'Yet to be payed'),
    )
    TYPE_CHOICES = (
        (1, 'First type'),
        (2, 'Second type'),
    )

    user = models.ForeignKey(User)

    buy_date = models.DateField(name="Buy date", null=True)
    end_date = models.DateField(name="End date", null=True)
    type = models.SmallIntegerField(name="Policy type", null=False, blank=False,
                               choices=TYPE_CHOICES)
    payment = models.CharField(name="Payment", max_length=10, null=False, blank=False, default="unpayed",
                               choices=PAYMENT_CHOICES)
    state = models.CharField(name="Policy state", max_length=10, null=False, blank=False, default="init",
                             choices=STATE_CHOICES)
    
