from django.contrib import admin

from slots.models import TimeSlot, AppointmentSlot

# Register your models here.
admin.site.register(AppointmentSlot)
admin.site.register(TimeSlot)
