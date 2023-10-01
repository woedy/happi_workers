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

            appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']
            if appointer.user_type in appointer_list:
                for slot in availability:
                    slot_date = slot.get('date')

                    # Check if a slot with the same date already exists
                    existing_slot = AppointmentSlot.objects.filter(user_id=appointer, slot_date=slot_date).first()
                    if existing_slot:
                        errors['availability'] = ['Slot with the same date already exists.']
                        break

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
        date = request.data.get('date', "")
        time_slots = request.data.get('time_slots', "")
        timezone = request.data.get('timezone', "")

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']



        if not date:
            errors['date'] = ['Date is required.']




        if not time_slots:
            errors['time_slots'] = ['At least 1 Time slot is required.']

        if not timezone:
            errors['timezone'] = ['Timezone is required.']


        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        appointer = User.objects.get(user_id=pract_id)

        all_app_slots = AppointmentSlot.objects.all().filter(user_id=appointer)

        print(all_app_slots)
        if not all_app_slots:

            appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']
            if appointer.user_type in appointer_list:
                new_slot = AppointmentSlot.objects.create(
                    user_id=appointer,
                    slot_date=date
                )
            for time in time_slots:
                new_time_slot = TimeSlot.objects.create(
                    appointment_slot=new_slot,
                    time=time
                )
                new_slot.time_slot_count = len(time_slots)
                new_slot.save()
        else:
            for slot in all_app_slots:
                print(slot.slot_date)
                print(date)
                if str(slot.slot_date) == date:
                    errors['date'] = ['This slot is already occupied.']
                elif str(slot.slot_date) != date:
                    appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']
                    ##
                    if appointer.user_type in appointer_list:
                        new_slot = AppointmentSlot.objects.create(
                            user_id=appointer,
                            slot_date=date
                        )
                    ##
                    for time in time_slots:
                        new_time_slot = TimeSlot.objects.create(
                            appointment_slot=new_slot,
                            time=time
                        )
                    new_slot.time_slot_count = len(time_slots)
                    new_slot.save()
        data['appointment_slot_id'] = new_slot.id



##
#
        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##


        payload['message'] = "Slot added successfully"
        payload['data'] = data

        return Response(payload)


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


        try:
            for old_slot in availability:
                slot = AppointmentSlot.objects.get(id=old_slot['slot_id'])
                slot.slot_date = old_slot['date']
                slot.save()

                time_slots_data = TimeSlot.objects.all().filter(appointment_slot=slot)
                for time in time_slots_data:
                    time.delete()

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







