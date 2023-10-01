from django.contrib.auth import get_user_model
from rest_framework import serializers

from slots.models import AppointmentSlot, TimeSlot

User = get_user_model()


class OccupantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'full_name', 'phone', ]

class AppointmentTimeSerializer(serializers.ModelSerializer):
    occupant = OccupantSerializer(many=False)

    class Meta:
        model = TimeSlot
        fields = ['time', 'occupied', 'occupant', ]

class AppointmentSlotSerializer(serializers.ModelSerializer):

    slot_times = AppointmentTimeSerializer(many=True)

    class Meta:
        model = AppointmentSlot
        fields = ['id', 'slot_date', 'time_slot_count', 'state', 'slot_times']







#class AppointmentSlotSerializer(serializers.ModelSerializer):
#    def get_slot_times(self, obj):
#        # Get all related TimeSlot objects and extract their time values
#        return [time_slot.time for time_slot in obj.slot_times.all()]
#
#    slot_times = serializers.SerializerMethodField(method_name='get_slot_times')
#
#    class Meta:
#        model = AppointmentSlot
#        fields = ['id', 'slot_date', 'slot_times']
#