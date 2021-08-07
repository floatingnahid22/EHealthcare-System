from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userType(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    patient = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.user.username

class doctorInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    speciality = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    fees = models.IntegerField(null=True, blank=True)
    visitingHours = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.fullName

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()

    Morning_Slot = 'Morning Slot'
    Evening_Slot = 'Evening Slot'
    timeSlot_choices = [
        (Morning_Slot, 'Morning Slot'),
        (Evening_Slot, 'Evening Slot'),
    ]
    timeSlot = models.CharField(max_length=50, choices=timeSlot_choices)
