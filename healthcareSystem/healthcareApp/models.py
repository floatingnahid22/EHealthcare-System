from django.db import models
from django.contrib.auth.models import User
from .choices import *
from django_cryptography.fields import encrypt

# Create your models here.
# Model for User Registration Type(Patient/Doctor)
class userType(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    patient = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Model for Doctors Information
class doctorInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    speciality = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    hospitalName = models.CharField(max_length=200, null=True, blank=True)
    fees = models.IntegerField(null=True, blank=True)
    visitingHours = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='doctorsPP', null=True, blank=True)

    def __str__(self):
        return self.fullName


# Model for Patient Information
class patientInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phoneNumber = models.CharField(max_length=20, null=True, blank=True)
    DoB = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    Male = 'Male'
    Female = 'Female'
    gender_choices = [
        (Male, 'Male'),
        (Female, 'Female'),
    ]
    gender = models.CharField(max_length=50, choices=gender_choices, null=True, blank=True)
    bloodGroup = models.CharField(max_length=10, choices=Blood_Group_Choices, null=True, blank=True)
    bloodPressure = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.fullName


# Model for Appointment Information
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(doctorInfo, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(patientInfo, on_delete=models.CASCADE, null=True, blank=True)
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
