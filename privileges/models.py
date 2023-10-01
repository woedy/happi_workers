from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class AdminPrivilege(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_privilege")

    create_user = models.BooleanField(default=False,)
    edit_user = models.BooleanField(default=False, )
    delete_user = models.BooleanField(default=False, )

    create_practitioner = models.BooleanField(default=False, )
    edit_practitioner = models.BooleanField(default=False, )
    delete_practitioner = models.BooleanField(default=False, )

    view_appointments = models.BooleanField(default=False, )
    create_appointments = models.BooleanField(default=False, )
    modify_appointments = models.BooleanField(default=False, )
    cancel_appointments = models.BooleanField(default=False, )

    access_calender = models.BooleanField(default=False, )
    modify_calender = models.BooleanField(default=False, )

    generate_reports = models.BooleanField(default=False, )

    view_transactions = models.BooleanField(default=False, )
    modify_transaction_status = models.BooleanField(default=False, )

    email_notification_settings = models.BooleanField(default=False, )

    customer_support = models.BooleanField(default=False, )

    logs_access = models.BooleanField(default=False, )



class PractitionerPrivilege(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="practitioner_privilege")

    view_clients = models.BooleanField(default=False, )
    view_client_detail = models.BooleanField(default=False, )
    create_client = models.BooleanField(default=False, )
    edit_client = models.BooleanField(default=False, )
    delete_client = models.BooleanField(default=False, )

    view_calender = models.BooleanField(default=False, )
    set_availability = models.BooleanField(default=False, )
    time_off = models.BooleanField(default=False, )

    create_appointment = models.BooleanField(default=False, )
    edit_appointment = models.BooleanField(default=False, )
    delete_appointment = models.BooleanField(default=False, )

    edit_profile = models.BooleanField(default=False, )

    sms_notification = models.BooleanField(default=False, )
    email_notification = models.BooleanField(default=False, )
    push_notification = models.BooleanField(default=False, )

    view_earnings = models.BooleanField(default=False, )
    payment_history = models.BooleanField(default=False, )

    report_access = models.BooleanField(default=False, )


class ClientPrivilege(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_privilege")

    view_practitioners = models.BooleanField(default=False, )
    book_appointment = models.BooleanField(default=False, )

    edit_profile = models.BooleanField(default=False, )

    view_history = models.BooleanField(default=False, )

    change_status = models.BooleanField(default=False, )
    can_cancel = models.BooleanField(default=False, )
    can_reschedule = models.BooleanField(default=False, )

    payment_history = models.BooleanField(default=False, )
    make_payment = models.BooleanField(default=False, )
    access_invoice = models.BooleanField(default=False, )




class HumanResourcesPrivilege(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hr_privilege")

    add_client = models.BooleanField(default=False, )
    remove_client = models.BooleanField(default=False, )
    book_client = models.BooleanField(default=False, )




class AppointeePrivilege(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointee_privilege")

    view_practitioners = models.BooleanField(default=False, )
    book_appointment = models.BooleanField(default=False, )

    edit_profile = models.BooleanField(default=False, )

    view_history = models.BooleanField(default=False, )

    change_status = models.BooleanField(default=False, )
    can_cancel = models.BooleanField(default=False, )
    can_reschedule = models.BooleanField(default=False, )

    payment_history = models.BooleanField(default=False, )
    make_payment = models.BooleanField(default=False, )
    access_invoice = models.BooleanField(default=False, )




class AppointerPrivilege(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointer_privilege")

    view_clients = models.BooleanField(default=False, )
    view_client_detail = models.BooleanField(default=False, )
    create_client = models.BooleanField(default=False, )
    edit_client = models.BooleanField(default=False, )
    delete_client = models.BooleanField(default=False, )

    view_calender = models.BooleanField(default=False, )
    set_availability = models.BooleanField(default=False, )
    time_off = models.BooleanField(default=False, )

    create_appointment = models.BooleanField(default=False, )
    edit_appointment = models.BooleanField(default=False, )
    delete_appointment = models.BooleanField(default=False, )

    edit_profile = models.BooleanField(default=False, )

    sms_notification = models.BooleanField(default=False, )
    email_notification = models.BooleanField(default=False, )
    push_notification = models.BooleanField(default=False, )

    view_earnings = models.BooleanField(default=False, )
    payment_history = models.BooleanField(default=False, )

    report_access = models.BooleanField(default=False, )

