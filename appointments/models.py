from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save

from mysite.utils import unique_appointment_id_generator

User = settings.AUTH_USER_MODEL




class AppointmentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()

        if query is not None:
            or_lookup = (
                    Q(patient__last_name__icontains=query) |
                    Q(patient__first_name__icontains=query) |
                    Q(status__icontains=query ) |
                    Q(appointment_type__icontains=query) |
                    Q(appointment_medium__icontains=query) |
                    Q(doctor__user__last_name__icontains=query)

            )

            qs = qs.filter(or_lookup).distinct()
        return qs


APPOINTMENT_TYPE_CHOICES = (
    ('Complain', 'Complain'),
    ('Therapy', 'Therapy'),
    ('Just talk', 'Just talk'),

)

APPOINTMENT_MEDIUM_CHOICES = (
    ('Video Call', 'Video Call'),
    ('Voice Call', 'Voice Call'),
    ('Text Message', 'Text Message'),
    ('Walk in', 'Walk in'),


)



APPOINTMENT_PAYMENT_METHOD_CHOICES = (
    ('Momo', 'Momo'),
    ('Paypal', 'Paypal'),
    ('Bank', 'Bank'),
)


STATUS_CHOICE = (

    ('Created', 'Created'),
    ('Pending', 'Pending'),
    ('Rescheduled', 'Rescheduled'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),
    ('Started', 'Started'),
    ('Ongoing', 'Ongoing'),
    ('Review', 'Review'),
    ('Completed', 'Completed'),
    ('Canceled', 'Canceled'),
)




class GenericAppointment(models.Model):
    appointment_id = models.CharField(max_length=200, null=True, blank=True)

    appointer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointer")
    appointee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,  related_name="appointee")
    human_resource = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,  related_name="appointment_hr")
    app_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointment_admin")

    appointment_type = models.CharField(max_length=255, default="Therapy", null=True, blank=True, choices=APPOINTMENT_TYPE_CHOICES)
    appointment_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    appointment_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    time_zone = models.CharField(null=True, blank=True, max_length=100)
    appointment_medium = models.CharField(max_length=255, default="Walk in", null=True, blank=True, choices=APPOINTMENT_MEDIUM_CHOICES)

    reason = models.TextField(null=True, blank=True)
    re_scheduled = models.BooleanField(default=False)

    amount_to_pay = models.CharField(null=True, blank=True, max_length=100)
    actual_price = models.CharField(null=True, blank=True, max_length=100)

    actual_duration = models.CharField(null=True, blank=True, max_length=100)

    review = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=STATUS_CHOICE)

    appointment_start = models.DateTimeField(null=True, blank=True)
    appointment_end = models.DateTimeField(null=True, blank=True)

    appointment_rescheduled_at = models.DateTimeField(null=True, blank=True)
    appointment_approved_at = models.DateTimeField(null=True, blank=True)
    appointment_declined_at = models.DateTimeField(null=True, blank=True)
    appointment_cancelled_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppointmentManager()




def pre_save_appointment_id_generator(sender, instance, *args, **kwargs):
    if not instance.appointment_id:
        instance.appointment_id = unique_appointment_id_generator(instance)

pre_save.connect(pre_save_appointment_id_generator, sender=GenericAppointment)

