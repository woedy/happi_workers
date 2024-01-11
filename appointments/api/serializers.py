from django.contrib.auth import get_user_model
from rest_framework import serializers

from appointments.models import GenericAppointment
from slots.models import AppointmentSlot, TimeSlot

User = get_user_model()

class AppUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'full_name',
        ]

class GenericAppointmentSerializer(serializers.ModelSerializer):
    appointer = AppUserSerializer(many=False)
    appointee = AppUserSerializer(many=False)

    class Meta:
        model = GenericAppointment
        fields = [
            'appointment_id',
            'appointer',
            'appointee',
            'human_resource',
            'app_admin',

            'appointment_type',
            'appointment_date',
            'appointment_time',


            're_scheduled',

            'actual_duration',

            'status',

            'appointment_start',
            'appointment_end',

            'appointment_rescheduled_at',
            'appointment_approved_at',
            'appointment_declined_at',
            'appointment_cancelled_at',

            'created_at',

        ]



class ListPractGenericAppointmentSerializer(serializers.ModelSerializer):
    appointee = AppUserSerializer(many=False)

    class Meta:
        model = GenericAppointment
        fields = [
            'appointment_id',
            'appointee',
            'appointment_date',
            'appointment_time',
            'status',

            'appointment_start',
            'appointment_end',

            'created_at'
        ]





class ListClientGenericAppointmentSerializer(serializers.ModelSerializer):
    appointer = AppUserSerializer(many=False)

    class Meta:
        model = GenericAppointment
        fields = [
            'appointment_id',
            'appointer',
            'appointment_date',
            'appointment_time',
            'status',

            'appointment_start',
            'appointment_end',

            'created_at'
        ]




