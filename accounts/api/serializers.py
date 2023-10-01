from django.contrib.auth import get_user_model
from rest_framework import serializers

from privileges.models import AppointerPrivilege, HumanResourcesPrivilege, AdminPrivilege, AppointeePrivilege
from slots.models import AppointmentSlot, TimeSlot

User = get_user_model()


class AdminPrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminPrivilege
        fields = ['id',
                  'create_user',
                  'edit_user',
                  'delete_user',

                  'create_practitioner',
                  'edit_practitioner',
                  'delete_practitioner',

                  'view_appointments',
                  'create_appointments',
                  'modify_appointments',
                  'cancel_appointments',

                  'access_calender',
                  'modify_calender',

                  'generate_reports',

                  'view_transactions',
                  'modify_transaction_status',

                  'email_notification_settings',
                  'customer_support',
                  'logs_access',


                  ]


class HumanResourcesPrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HumanResourcesPrivilege
        fields = ['id',
                  'add_client',
                  'remove_client',
                  'book_client',
                  ]


class AppointeePrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointeePrivilege
        fields = ['id',
                  'view_practitioners',
                  'book_appointment',

                  'edit_profile',
                  'view_history',
                  'change_status',


                  'can_cancel',
                  'can_reschedule',

                  'payment_history',

                  'make_payment',
                  'access_invoice',



                  ]


class AppointerPrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointerPrivilege
        fields = ['id',
                  'view_clients',
                  'view_client_detail',
                  'create_client',
                  'edit_client',
                  'delete_client',

                  'view_calender',
                  'set_availability',
                  'time_off',

                  'create_appointment',
                  'edit_appointment',
                  'delete_appointment',

                  'edit_profile',

                  'sms_notification',
                  'email_notification',
                  'push_notification',

                  'view_earnings',
                  'payment_history',
                  'report_access',

                  ]
