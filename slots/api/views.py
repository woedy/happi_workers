from datetime import datetime, date, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from accounts.models import Company
from activities.models import AllActivity
from slots.api.serializers import AppointmentSlotSerializer
from slots.models import AppointmentSlot, TimeSlot

User = get_user_model()



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_appointer_slot(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        timezone = request.data.get('timezone', "")
        availability = request.data.get('availability', [])

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not timezone:
            errors['timezone'] = ['Timezone is required.']

        if not availability:
            errors['availability'] = ['Availability is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointer = User.objects.get(user_id=pract_id)
            interval = appointer.availability_interval

            if interval is None:
                errors['availability'] = [f'Please set your availability interval first.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the existing slots for the practitioner
            existing_slots = AppointmentSlot.objects.filter(user_id=appointer)
            existing_slot_dates = existing_slots.values_list('slot_date', flat=True)

            appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']
            if appointer.user_type in appointer_list:
                for slot_data in availability:
                    slot_date = slot_data.get('date')
                    new_time_slots = slot_data.get('time_slots')

                    # Convert the times to datetime objects
                    time_objects = [datetime.strptime(t, "%H:%M:%S" if len(t) > 5 else "%H:%M").time() for t in slot_data['time_slots']]

                    # # Check if the times are at least  hours apart
                    # if not are_times_spaced(interval, time_objects):
                    #     errors['availability'] = [f'Times provided should be at least {interval} apart.']
                    #     payload['message'] = "Errors"
                    #     payload['errors'] = errors
                    #     return Response(payload, status=status.HTTP_400_BAD_REQUEST)

                    # Check if a slot with the same date already exists
                    existing_slot = existing_slots.filter(slot_date=slot_date).first()

                    if existing_slot:
                        # Slot already exists, update it
                        existing_time_slots = TimeSlot.objects.filter(appointment_slot=existing_slot)

                        # Iterate through the new time slots
                        for time in new_time_slots:
                            existing_time_slot = existing_time_slots.filter(time=time).first()
                            if existing_time_slot:
                                if existing_time_slot.occupied:
                                    # Time slot is occupied, continue to the next slot
                                    continue
                            else:
                                # Create a new time slot if it doesn't exist
                                TimeSlot.objects.create(
                                    appointment_slot=existing_slot,
                                    time=time,
                                    occupied=False
                                )
                        # Delete time slots that are not in the new list
                        existing_time_slots.filter(~Q(time__in=new_time_slots)).delete()
                    else:
                        # Slot doesn't exist, create a new slot
                        new_slot = AppointmentSlot.objects.create(user_id=appointer, slot_date=slot_date)
                        for time in new_time_slots:
                            TimeSlot.objects.create(
                                appointment_slot=new_slot,
                                time=time,
                                occupied=False
                            )

                # Delete slots that are not in the new list
                existing_slots.filter(~Q(slot_date__in=[s['date'] for s in availability])).delete()

        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Slot added or updated successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_appointer_slot4444(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        timezone = request.data.get('timezone', "")
        availability = request.data.get('availability', [])

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not timezone:
            errors['timezone'] = ['Timezone is required.']

        if not availability:
            errors['availability'] = ['Availability is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointer = User.objects.get(user_id=pract_id)
            interval = appointer.availability_interval

            if interval is None:
                errors['availability'] = [f'Please set your availability interval first.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the existing slots for the practitioner
            existing_slots = AppointmentSlot.objects.filter(user_id=appointer)
            existing_slot_dates = existing_slots.values_list('slot_date', flat=True)

            appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']
            if appointer.user_type in appointer_list:
                for slot_data in availability:
                    slot_date = slot_data.get('date')
                    new_time_slots = slot_data.get('time_slots')

                    # Check if a slot with the same date already exists
                    existing_slot = existing_slots.filter(slot_date=slot_date).first()

                    if existing_slot:
                        # Slot already exists, update it
                        existing_time_slots = TimeSlot.objects.filter(appointment_slot=existing_slot)

                        # Iterate through the new time slots
                        for time in new_time_slots:
                            existing_time_slot = existing_time_slots.filter(time=time).first()
                            if existing_time_slot:
                                if existing_time_slot.occupied:
                                    # Time slot is occupied, continue to the next slot
                                    continue
                            else:
                                # Create a new time slot if it doesn't exist
                                TimeSlot.objects.create(
                                    appointment_slot=existing_slot,
                                    time=time,
                                    occupied=False
                                )
                        # Delete time slots that are not in the new list
                        existing_time_slots.filter(~Q(time__in=new_time_slots)).delete()
                    else:
                        # Slot doesn't exist, create a new slot
                        new_slot = AppointmentSlot.objects.create(user_id=appointer, slot_date=slot_date)
                        for time in new_time_slots:
                            TimeSlot.objects.create(
                                appointment_slot=new_slot,
                                time=time,
                                occupied=False
                            )

                # Delete slots that are not in the new list
                existing_slots.filter(~Q(slot_date__in=[s['date'] for s in availability])).delete()

        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Slot added or updated successfully"
        payload['data'] = data

        return Response(payload)






@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_appointer_slot333333(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        timezone = request.data.get('timezone', "")
        availability = request.data.get('availability', [])

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not timezone:
            errors['timezone'] = ['Timezone is required.']

        if not availability:
            errors['availability'] = ['Availability is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointer = User.objects.get(user_id=pract_id)

            interval = appointer.availability_interval

            if interval is None:
                errors['availability'] = [f'Please set your availability interval first.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the existing slots for the practitioner
            existing_slots = AppointmentSlot.objects.filter(user_id=appointer)

            appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']
            if appointer.user_type in appointer_list:
                for slot_data in availability:
                    slot_date = slot_data.get('date')

                    # Check if a slot with the same date already exists
                    existing_slot = existing_slots.filter(slot_date=slot_date).first()

                    if existing_slot:
                        # If the slot exists, check for occupied time slots
                        occupied_time_slots = existing_slot.slot_times.filter(occupied=True)
                        new_time_slots = slot_data.get('time_slots')

                        # Remove unoccupied time slots
                        unoccupied_time_slots = [time for time in new_time_slots if time not in occupied_time_slots]

                        if unoccupied_time_slots:
                            # Update the slot with unoccupied time slots
                            existing_slot.slot_times.filter(time__in=unoccupied_time_slots).delete()
                        else:
                            # All time slots are occupied, continue to the next slot
                            continue
                    else:
                        unoccupied_time_slots = slot_data.get('time_slots')

                    # Create or update the slot with the new time slots
                    new_slot, created = AppointmentSlot.objects.get_or_create(
                        user_id=appointer,
                        slot_date=slot_date
                    )

                    for time in unoccupied_time_slots:
                        TimeSlot.objects.create(
                            appointment_slot=new_slot,
                            time=time,
                            occupied=False  # Ensure that new slots are marked as unoccupied
                        )

                    # Update the time slot count for the slot
                    new_slot.time_slot_count = len(unoccupied_time_slots)
                    new_slot.save()

                    # Add new ACTIVITY
                    new_activity = AllActivity.objects.create(
                        user=User.objects.get(id=1),
                        subject="Availability set",
                        body=f"{appointer.full_name} just added their availability."
                    )
                    new_activity.save()
        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Slot added or updated successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_appointer_slot222(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        timezone = request.data.get('timezone', "")
        availability = request.data.get('availability', "")

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not timezone:
            errors['timezone'] = ['Timezone is required.']

        if not availability:
            errors['availability'] = ['Availability is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointer = User.objects.get(user_id=pract_id)

            interval = appointer.availability_interval

            if interval is None:
                errors['availability'] = [f'Please set your availability interval first.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)


            appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']
            if appointer.user_type in appointer_list:
                for slot in availability:
                    slot_date = slot.get('date')

                    # Check if a slot with the same date already exists
                    existing_slot = AppointmentSlot.objects.filter(user_id=appointer, slot_date=slot_date).first()
                    if existing_slot:
                        errors['availability'] = ['Slot with the same date already exists.']
                        break

                    # Convert the times to datetime objects
                    time_objects = [datetime.strptime(t, "%H:%M:%S" if len(t) > 5 else "%H:%M").time() for t in slot['time_slots']]

                    # Check if the times are at least  hours apart
                    if not are_times_spaced(interval, time_objects):
                        errors['availability'] = [f'Times provided should be at least {interval} apart.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



                    new_slot = AppointmentSlot.objects.create(
                        user_id=appointer,
                        slot_date=slot_date
                    )





                    for time in slot['time_slots']:
                        new_time_slot = TimeSlot.objects.create(
                            appointment_slot=new_slot,
                            time=time
                        )
                        new_slot.time_slot_count = len(slot['time_slots'])
                        new_slot.save()

                        # Add new ACTIVITY
                        new_activity = AllActivity.objects.create(
                            user=User.objects.get(id=1),
                            subject="Availability set",
                            body=f"{appointer.full_name} just added their availability."
                        )
                        new_activity.save()
        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Slot added successfully"
        payload['data'] = data

        return Response(payload)


def are_times_spaced(interval, times):
    # Calculate the minimum required time difference in minutes
    required_minutes = get_interval_in_minutes(interval)

    for i in range(1, len(times)):
        time_difference = calculate_time_difference(times[i], times[i - 1])
        if time_difference < required_minutes:
            return False

    return True





def get_interval_in_minutes(interval):
    intervals = {
        '1 hour': 1 * 60,
        '6 hours': 6 * 60,
        '8 hours': 8 * 60,
        '12 hours': 12 * 60,
        '24 hours': 24 * 60,
        '48 hours': 48 * 60,
    }
    return intervals.get(interval, 0)

def calculate_time_difference(time1, time2):
    dt1 = datetime.combine(date.today(), time1)
    dt2 = datetime.combine(date.today(), time2)
    return (dt1 - dt2).total_seconds() / 60


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def update_appointer_slot(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")

        availability = request.data.get('availability', "")

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']


        if not availability:
            errors['availability'] = ['Availability is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        appointer = User.objects.get(user_id=pract_id)
        interval = appointer.availability_interval

        if interval is None:
            errors['availability'] = [f'Please set your availability interval first.']
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:

            for old_slot in availability:
                slot = AppointmentSlot.objects.get(id=old_slot['slot_id'])
                slot.slot_date = old_slot['date']
                slot.save()

                time_slots_data = TimeSlot.objects.all().filter(appointment_slot=slot)
                for time in time_slots_data:
                    time.delete()

                # Convert the times to datetime objects
                time_objects = [datetime.strptime(t, "%H:%M:%S" if len(t) > 5 else "%H:%M").time() for t in old_slot['time_slots']]

                # Check if the times are at least  hours apart
                if not are_times_spaced(interval, time_objects):
                    errors['availability'] = [f'Times provided should be at least {interval} apart.']
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)


            for time in old_slot['time_slots']:
                    new_time_slot = TimeSlot.objects.create(
                        appointment_slot=slot,
                        time=time
                    )

                    # Add new ACTIVITY
                    new_activity = AllActivity.objects.create(
                        user=User.objects.get(id=1),
                        subject="Availability Updated",
                        body=f"An appointee just updated their availability."
                    )
                    new_activity.save()

        except AppointmentSlot.DoesNotExist:
            errors['slot_id'] = ['Object is removed.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##
        #data['appintment_slot_id'] = slot.id

        payload['message'] = "Slot updated successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def update_appointer_slot222(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        slot_id = request.data.get('slot_id', "")
        date = request.data.get('date', "")
        time_slots = request.data.get('time_slots', "")

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not date:
            errors['date'] = ['Date is required.']

        if not time_slots:
            errors['time_slots'] = ['At least 1 Time slot is required.']




        company = Company.objects.get(company_id=company_id)

        try:
            slot = AppointmentSlot.objects.get(id=slot_id)
            slot.slot_date = date
            slot.save()

            time_slots_data = TimeSlot.objects.all().filter(appointment_slot=slot)
            for time in time_slots_data:
                time.delete()

            for time in time_slots:
                new_time_slot = TimeSlot.objects.create(
                    appointment_slot=slot,
                    time=time
                )

        except AppointmentSlot.DoesNotExist:
            errors['slot_id'] = ['Object is removed.']






#
        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##
        data['appintment_slot_id'] = slot.id

        payload['message'] = "Slot updated successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_appointer_slot(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        slot_id = request.data.get('slot_id', "")


        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            slot = AppointmentSlot.objects.get(id=slot_id)
            slot.delete()
        except:
            errors['slot_id'] = ['Slot does not exist.']



        # Add new ACTIVITY
        new_activity = AllActivity.objects.create(
            user=User.objects.get(id=1),
            subject="Slot Removed",
            body=f"Slot Removed."
        )
        new_activity.save()

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##
        #data['appintment_slot_id'] = slot.id

        payload['message'] = "Slot removed successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def list_practitioner_availability(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointer = User.objects.get(user_id=pract_id)
            availability_interval = appointer.availability_interval
            data['availability_interval'] = availability_interval

            # Define time range based on the chosen interval
            now = timezone.now()
            if availability_interval == "1 hour":
                end_time = now + timedelta(hours=1)
            elif availability_interval == "6 hours":
                end_time = now + timedelta(hours=6)
            elif availability_interval == "12 hours":
                end_time = now + timedelta(hours=12)
            elif availability_interval == "8 hours":
                end_time = now + timedelta(hours=8)
            elif availability_interval == "24 hours":
                end_time = now + timedelta(hours=24)
            elif availability_interval == "48 hours":
                end_time = now + timedelta(hours=48)
            else:
                errors['availability_interval'] = ['Invalid availability interval.']

            if 'availability_interval' not in errors:
                # Query for available appointment slots beyond the defined time range
                available_slots = AppointmentSlot.objects.filter(
                    user_id=appointer,
                    slot_date__gte=now,  # Filter for slots with dates beyond or equal to the current date
                )

                available_slots_data = []
                for slot in available_slots:
                    time_slots = TimeSlot.objects.filter(
                        appointment_slot=slot,
                        time__gte=end_time,  # Filter for time slots beyond the end of the chosen interval
                        occupied=False,  # Consider only unoccupied time slots

                    ).values_list('time', flat=True)
                    available_slots_data.append({
                        'slot_date': slot.slot_date,
                        'time_slots': list(time_slots),
                    })

                data['available_practitioner_slots'] = available_slots_data

        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Successful"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def list_practitioner_availabilityWORKING(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")


        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']


        try:
            appointer = User.objects.get(user_id=pract_id)

            availability_interval = appointer.availability_interval
            data['availability_interval'] = availability_interval

            all_app_slots = AppointmentSlot.objects.all().filter(user_id=appointer)

            all_app_slots_serializer = AppointmentSlotSerializer(all_app_slots, many=True)
            if all_app_slots_serializer:
                _all_app_slots = all_app_slots_serializer.data
                data['all_practitioner_slots'] = _all_app_slots



        except:
            errors['client_id'] = ['Practitioner does not exist does not exist']


##
#
        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##
        #data['appintment_slot_id'] = new_slot.id

        payload['message'] = "Successful"
        payload['data'] = data

        return Response(payload)






@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_availability_interval(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        interval = request.data.get('interval', "")


        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not interval:
            errors['interval'] = ['Interval is required.']


        company = Company.objects.get(company_id=company_id)

        appointer = User.objects.get(user_id=pract_id)

        if appointer.user_type == "Practitioner":
            appointer.availability_interval = interval
            appointer.save()
        else:
            errors['pract_id'] = ['User is not a practitioner.']





        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##
        #data['appintment_slot_id'] = new_slot.id

        payload['message'] = "Successful, Availability interval set."
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_recurring_slot(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        timezone = request.data.get('timezone', "")

        start_date = request.data.get('start_date', "")
        end_date = request.data.get('end_date', "")
        time = request.data.get('time', "")
        frequency = request.data.get('frequency', "")

        repeat = request.data.get('repeat', 1)
        week_days = request.data.get('week_days', "")

        # Validate the parameters
        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']
        if not company_id:
            errors['company_id'] = ['Company ID is required.']
        if not timezone:
            errors['timezone'] = ['Timezone is required.']
        if not start_date:
            errors['start_date'] = ['Start date is required.']
        if not end_date:
            errors['end_date'] = ['End date is required.']
        if not time:
            errors['time'] = ['Time is required.']
        if not frequency:
            errors['frequency'] = ['Frequency is required.']
        if not repeat or repeat <= 0:
            errors['repeat'] = ['Repeat must be a positive integer.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointer = User.objects.get(user_id=pract_id)
        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Parse the date and time strings into datetime objects
        start_datetime = datetime.strptime(start_date + " " + time, "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(end_date + " " + time, "%Y-%m-%d %H:%M")

        slots = []

        if frequency != "Weekly":
            # Calculate recurring slots based on the provided parameters for other frequencies
            current_date = start_datetime
            while current_date <= end_datetime:
                slots.append(current_date)

                if frequency == "Daily":
                    current_date += timedelta(days=repeat)

                elif frequency == "Monthly":
                    next_month = current_date + relativedelta(months=repeat)
                    current_date = next_month.replace(day=1)
                elif frequency == "Yearly":
                    current_date += relativedelta(years=repeat)

        elif frequency == "Weekly":

            # Parse the week_days string to get a list of selected weekdays (0=Monday, 6=Sunday)

            selected_weekdays = [int(day) for day in week_days.split(',')]

            # Calculate recurring slots based on the provided parameters for weekly frequency

            slots = []

            current_date = start_datetime

            while current_date <= end_datetime:

                if current_date.weekday() in selected_weekdays:
                    slots.append(current_date.date())

                current_date += timedelta(days=1)

            # Adjust the slots for the repeat value

            adjusted_slots = []

            repeat_count = repeat  # Initialize the repeat_count

            for i, slot in enumerate(slots):

                if i % repeat_count == 0:
                    adjusted_slots.append(slot)

                    repeat_count = repeat  # Reset the repeat_count to the original value when adding a slot

            print("#############")
            print(adjusted_slots)
            for slot in adjusted_slots:
                print(slot)
                new_slot = AppointmentSlot.objects.create(
                    user_id=appointer,
                    slot_date=slot,
                    is_recurring=True
                )
                new_time_slot = TimeSlot.objects.create(
                    appointment_slot=new_slot,
                    time=time
                )
                new_slot.time_slot_count = 1
                new_slot.save()

        if frequency != "Weekly":
            for slot in slots:
                print(slot)
                new_slot = AppointmentSlot.objects.create(
                    user_id=appointer,
                    slot_date=str(slot).split(" ")[0],
                    is_recurring=True
                )
                new_time_slot = TimeSlot.objects.create(
                    appointment_slot=new_slot,
                    time=str(slot).split(" ")[1]
                )
                new_slot.time_slot_count = 1
                new_slot.save()




        # Add new ACTIVITY
        new_activity = AllActivity.objects.create(
            user=User.objects.get(id=1),
            subject="Availability set - recurring",
            body=f"{appointer.full_name} just added a recurring availability."
        )
        new_activity.save()


        #print(adjusted_slots)

#        print(len(adjusted_slots))

        # Store the slots in the AppointmentSlot

        payload['message'] = "Recurring slots added successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_recurring_list_slot(request):
    payload = {}
    data = {}
    errors = {}
    repeat = 1

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        timezone = request.data.get('timezone', "")
        frequency = request.data.get('frequency', "")

        availabilities = request.data.get('availabilities', [])


        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']
        if not company_id:
            errors['company_id'] = ['Company ID is required.']
        if not timezone:
            errors['timezone'] = ['Timezone is required.']
        if not frequency:
            errors['frequency'] = ['Frequency is required.']


        if not availabilities:
            errors['availabilities'] = ['Availability list is required.']


        for availability_data in availabilities:

            start_date = availability_data.get('start_date', "")
            end_date = availability_data.get('end_date', "")
            time = availability_data.get('time', "")

            week_days = availability_data.get('week_days', "")

            # Validate the parameters

            if not start_date:
                errors['start_date'] = ['Start date is required.']
            if not end_date:
                errors['end_date'] = ['End date is required.']
            if not time:
                errors['time'] = ['Time is required.']

            if not repeat or repeat <= 0:
                errors['repeat'] = ['Repeat must be a positive integer.']

            if errors:
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            try:
                company = Company.objects.get(company_id=company_id)
            except Company.DoesNotExist:
                errors['company_id'] = ['Company does not exist.']

            try:
                appointer = User.objects.get(user_id=pract_id)
            except User.DoesNotExist:
                errors['pract_id'] = ['Practitioner does not exist.']

            if errors:
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            # Parse the date and time strings into datetime objects
            start_datetime = datetime.strptime(start_date + " " + time, "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(end_date + " " + time, "%Y-%m-%d %H:%M")

            slots = []

            if frequency != "Weekly":
                # Calculate recurring slots based on the provided parameters for other frequencies
                current_date = start_datetime
                while current_date <= end_datetime:
                    slots.append(current_date)

                    if frequency == "Daily":
                        current_date += timedelta(days=repeat)

                    elif frequency == "Monthly":
                        next_month = current_date + relativedelta(months=repeat)
                        current_date = next_month.replace(day=1)
                    elif frequency == "Yearly":
                        current_date += relativedelta(years=repeat)

            elif frequency == "Weekly":

                # Parse the week_days string to get a list of selected weekdays (0=Monday, 6=Sunday)

                selected_weekdays = week_days

                # Calculate recurring slots based on the provided parameters for weekly frequency

                slots = []

                current_date = start_datetime

                while current_date <= end_datetime:

                    if current_date.weekday() in selected_weekdays:
                        slots.append(current_date.date())

                    current_date += timedelta(days=1)

                # Adjust the slots for the repeat value

                adjusted_slots = []

                repeat_count = repeat  # Initialize the repeat_count

                for i, slot in enumerate(slots):

                    if i % repeat_count == 0:
                        adjusted_slots.append(slot)

                        repeat_count = repeat  # Reset the repeat_count to the original value when adding a slot

                print("#############")
                print(adjusted_slots)
                for slot in adjusted_slots:
                    print(slot)
                    new_slot = AppointmentSlot.objects.create(
                        user_id=appointer,
                        slot_date=slot,
                        is_recurring=True
                    )
                    new_time_slot = TimeSlot.objects.create(
                        appointment_slot=new_slot,
                        time=time
                    )
                    new_slot.time_slot_count = 1
                    new_slot.save()

            if frequency != "Weekly":
                for slot in slots:
                    print(slot)
                    new_slot = AppointmentSlot.objects.create(
                        user_id=appointer,
                        slot_date=str(slot).split(" ")[0],
                        is_recurring=True
                    )
                    new_time_slot = TimeSlot.objects.create(
                        appointment_slot=new_slot,
                        time=str(slot).split(" ")[1]
                    )
                    new_slot.time_slot_count = 1
                    new_slot.save()

        # Add new ACTIVITY
        new_activity = AllActivity.objects.create(
            user=User.objects.get(id=1),
            subject="Availability set - recurring",
            body=f"{appointer.full_name} just added a recurring availability."
        )
        new_activity.save()


        #print(adjusted_slots)

#        print(len(adjusted_slots))

        # Store the slots in the AppointmentSlot

        payload['message'] = "Recurring slots added successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_recurring_list_slot2222(request):
    payload = {}
    data = {}
    errors = {}
    frequency = "Weekly"
    repeat = 1

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        timezone = request.data.get('timezone', "")

        startRecur = request.data.get('startRecur', "")
        endRecur = request.data.get('endRecur', "")
        startTime = request.data.get('startTime', "")

        daysOfWeek = request.data.get('daysOfWeek', "")

        # Validate the parameters
        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']
        if not company_id:
            errors['company_id'] = ['Company ID is required.']
        if not timezone:
            errors['timezone'] = ['Timezone is required.']
        if not startRecur:
            errors['startRecur'] = ['Start date is required.']
        if not endRecur:
            errors['endRecur'] = ['End date is required.']
        if not startTime:
            errors['startTime'] = ['Time is required.']
        if not frequency:
            errors['frequency'] = ['Frequency is required.']
        if not repeat or repeat <= 0:
            errors['repeat'] = ['Repeat must be a positive integer.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointer = User.objects.get(user_id=pract_id)
        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Parse the date and time strings into datetime objects
        start_datetime = datetime.strptime(startRecur + " " + startTime, "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(endRecur + " " + startTime, "%Y-%m-%d %H:%M")

        slots = []

        if frequency != "Weekly":
            # Calculate recurring slots based on the provided parameters for other frequencies
            current_date = start_datetime
            while current_date <= end_datetime:
                slots.append(current_date)

                if frequency == "Daily":
                    current_date += timedelta(days=repeat)

                elif frequency == "Monthly":
                    next_month = current_date + relativedelta(months=repeat)
                    current_date = next_month.replace(day=1)
                elif frequency == "Yearly":
                    current_date += relativedelta(years=repeat)

        elif frequency == "Weekly":

            # Parse the week_days string to get a list of selected weekdays (0=Monday, 6=Sunday)

            selected_weekdays = daysOfWeek

            # Calculate recurring slots based on the provided parameters for weekly frequency

            slots = []

            current_date = start_datetime

            while current_date <= end_datetime:

                if current_date.weekday() in selected_weekdays:
                    slots.append(current_date.date())

                current_date += timedelta(days=1)

            # Adjust the slots for the repeat value

            adjusted_slots = []

            repeat_count = repeat  # Initialize the repeat_count

            for i, slot in enumerate(slots):

                if i % repeat_count == 0:
                    adjusted_slots.append(slot)

                    repeat_count = repeat  # Reset the repeat_count to the original value when adding a slot

            print("#############")
            print(adjusted_slots)
            for slot in adjusted_slots:
                print(slot)
                new_slot = AppointmentSlot.objects.create(
                    user_id=appointer,
                    slot_date=slot,
                    is_recurring=True
                )
                new_time_slot = TimeSlot.objects.create(
                    appointment_slot=new_slot,
                    time=startTime
                )
                new_slot.time_slot_count = 1
                new_slot.save()

        if frequency != "Weekly":
            for slot in slots:
                print(slot)
                new_slot = AppointmentSlot.objects.create(
                    user_id=appointer,
                    slot_date=str(slot).split(" ")[0],
                    is_recurring=True
                )
                new_time_slot = TimeSlot.objects.create(
                    appointment_slot=new_slot,
                    time=str(slot).split(" ")[1]
                )
                new_slot.time_slot_count = 1
                new_slot.save()




        # Add new ACTIVITY
        new_activity = AllActivity.objects.create(
            user=User.objects.get(id=1),
            subject="Availability set - recurring",
            body=f"{appointer.full_name} just added a recurring availability."
        )
        new_activity.save()


        #print(adjusted_slots)

#        print(len(adjusted_slots))

        # Store the slots in the AppointmentSlot

        payload['message'] = "Recurring slots added successfully"
        payload['data'] = data

        return Response(payload)

