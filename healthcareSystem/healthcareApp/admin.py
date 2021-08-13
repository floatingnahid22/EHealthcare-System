from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(userType)
admin.site.register(doctorInfo)
admin.site.register(patientInfo)
admin.site.register(Appointment)