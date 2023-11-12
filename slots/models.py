from django.conf import settings
from django.db import models


# Create your models here.

User = settings.AUTH_USER_MODEL

SLOT_STATE_CHOICES = (
    ("Vacant", "Vacant"),
    ("Partial", "Partial"),
    ("Occupied", "Occupied")
)
class AppointmentSlot(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointer_slot")

    slot_date = models.DateField(null=True, blank=True)
    time_slot_count = models.IntegerField(default=0)
    state = models.CharField(default="Vacant", choices=SLOT_STATE_CHOICES, max_length=255)

    is_recurring = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class TimeSlot(models.Model):
    appointment_slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name="slot_times")
    #appointment = models.ForeignKey(GenericAppointment, null=True, blank=True, on_delete=models.SET_NULL, related_name="slot_appointment")
    appointment_id = models.IntegerField(null=True, blank=True)

    time = models.TimeField(null=True, blank=True)


    occupied = models.BooleanField(default=False)
    occupant = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="appointment_occupant")

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


FREQUENCY_CHOICES = [
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('Yearly', 'Yearly')
]


class RecurringSlot(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recurring_slot")
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    week_days = models.CharField(max_length=122, null=True, blank=True)

    repeat = models.IntegerField(default=1)
    start_time = models.TimeField()
    end_time = models.TimeField()



class SingleSlot(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="single_slot")
    title = models.CharField(max_length=122, null=True, blank=True)

    start_date = models.DateTimeField()
    date = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ListRecurringSlot(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_slot")
    title = models.CharField(max_length=122, null=True, blank=True)
    days_of_week = models.CharField(max_length=10, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField(null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




REPEAT_ON_CHOICES = [
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('Yearly', 'Yearly')
]



END_REPEAT_CHOICES = [
    ('Never', 'Never'),
    ('on', 'on'),
    ('After', 'After'),
]

MONTH_CHOICES = [
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
]


class PlummHealthRecurring(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plum_recurring")
    start_date = models.DateField()
    end_date = models.DateField()

    repeat = models.CharField(max_length=10, choices=REPEAT_ON_CHOICES)
    repeat_every = models.IntegerField(default=1)



    repeat_on = models.CharField(max_length=10, null=True, blank=True)
    repeat_on_day = models.IntegerField(default=1)
    repeat_on_month = models.CharField(max_length=10, choices=MONTH_CHOICES, null=True, blank=True)



    end_repeat = models.CharField(max_length=10, choices=END_REPEAT_CHOICES)
    end_repeat_on = models.DateField(null=True, blank=True)
    end_repeat_after = models.IntegerField(default=1)

