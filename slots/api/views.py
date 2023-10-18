from datetime import datetime, date, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
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

        print(adjusted_slots)

        print(len(adjusted_slots))

        # Store the slots in the AppointmentSlot

        payload['message'] = "Recurring slots added successfully"
        payload['data'] = data

        return Response(payload)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_recurring_slot2222222(request):
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

        repeat = request.data.get('repeat', "")

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

        if not repeat:
            errors['repeat'] = ['Repeat is required.']


        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointer = User.objects.get(user_id=pract_id)

            #### Daily Logic
            if frequency == "Daily":
                print("#############")
                print("Daily")
                slots = []

            #### Weekly Logic

            if frequency == "Weekly":
                print("#############")
                print("Weekly")



            #### Monthly Logic

            if frequency == "Monthly":
                print("#############")
                print("Monthly")


            #### Yearly Logic

            if frequency == "Yearly":
                print("#############")
                print("Yearly")


        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Recurring slots added successfully"
        payload['data'] = data

        return Response(payload)


