import django_filters
from .models import *

class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = ['timeSlot']