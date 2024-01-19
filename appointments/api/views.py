from datetime import datetime

from celery import chain
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.dateparse import parse_time
from rest_framework import status
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.response import Response

from accounts.models import Company
from activities.models import AllActivity
from appointments.api.serializers import GenericAppointmentSerializer, \
    ListPractGenericAppointmentSerializer, ListClientGenericAppointmentSerializer
from appointments.models import GenericAppointment
from slots.models import AppointmentSlot, TimeSlot
from happi_project.tasks import send_client_email, send_practitioner_email

User = get_user_model()



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        slot_id = request.data.get('slot_id', "")
        slot_time = request.data.get('slot_time', "")

        if not client_id:
            errors['client_id'] = ['Client User ID is required.']

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot id is required.']

        if not slot_time:
            errors['slot_time'] = ['Slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(slot_time) < 8:
                slot_time += ':00'
        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            client = User.objects.get(user_id=client_id)
        except User.DoesNotExist:
            errors['client_id'] = ['Client does not exist']

        try:
            practitioner = User.objects.get(user_id=pract_id)
        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist']

        try:
            app_slot = AppointmentSlot.objects.get(id=slot_id)

            admin = User.objects.filter(company=company, user_type="Admin").first()

            # Check if there's already an appointment for the same date and time
            existing_appointment = GenericAppointment.objects.filter(
                slot=app_slot,
                appointment_time=slot_time,
                appointee=client,
                appointer=practitioner,
            ).first()

            if existing_appointment:
                errors['slot_date'] = ['Appointment for this date and time already exists.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)



            # Check for appointment interval
            _slot_date = app_slot.slot_date
            pract_interval = practitioner.availability_interval


            new_appointment = GenericAppointment.objects.create(
                appointer=practitioner,
                appointee=client,
                app_admin=admin,
                slot=app_slot,
                appointment_date=app_slot.slot_date,
                appointment_time=slot_time,
            )

            app_slot.state = "Partial"
            app_slot.save()

            slot_times = TimeSlot.objects.filter(appointment_slot=app_slot)

            for time in slot_times:
                if str(time.time) == str(slot_time):
                    print("################")
                    print("The time is in the database")
                    if time.occupied:
                        errors['slot_time'] = ['Slot time is already occupied.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
                    elif not time.occupied:
                        time.occupied = True
                        time.occupant = client
                        time.appointment_id = new_appointment.id
                        time.save()

            occupied_count = TimeSlot.objects.filter(appointment_slot=app_slot, occupied=True)

            if len(occupied_count) == app_slot.time_slot_count:
                app_slot.state = "Occupied"
                app_slot.save()

            # SEND CLIENT EMAIL
            client_subject = f"Yay! Your Appointment with {practitioner.full_name} is Confirmed 🎉"
            client_content = f"Hey {client.full_name},\nGuess what? Your appointment with {practitioner.full_name} on {new_appointment.appointment_date} at {new_appointment.appointment_time} is all set! 🌟\n\nMark your calendar and set your reminders because we can't wait to see you!\n\nCheers,\n\nThe {company.company_name} Team"

            # SEND PRACTITIONER EMAIL
            pract_subject = f"New Appointment Alert!🚨"
            pract_content = f"Hello {practitioner.full_name},\n\nGreat news! {client.full_name} has booked an appointment with you on {new_appointment.appointment_date} at {new_appointment.appointment_time}. Time to show off your skills!🌟\n\nBest,\n\nThe {company.company_name} Team"

            # Use Celery chain to execute tasks in sequence
            email_chain = chain(
                send_client_email.si(client_subject, client_content, client.email),
                send_practitioner_email.si(pract_subject, pract_content, practitioner.email),
            )

            # Execute the Celery chain asynchronously
            email_chain.apply_async()


            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=new_appointment.app_admin,
                subject="New Appointment Set",
                body=f"New appointment set between {practitioner.full_name} and {client.full_name} on {new_appointment.appointment_date} at {new_appointment.appointment_time}"
            )
            new_activity.save()

            data['appointment_id'] = new_appointment.appointment_id
            payload['data'] = data

        except AppointmentSlot.DoesNotExist:
            errors['slot_id'] = ['Slot does not exist']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment added successfully"
        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_appointment_view3333333333(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        slot_id = request.data.get('slot_id', "")
        slot_time = request.data.get('slot_time', "")

        if not client_id:
            errors['client_id'] = ['Client User ID is required.']

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot id is required.']

        if not slot_time:
            errors['slot_time'] = ['Slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(slot_time) < 8:
                slot_time += ':00'
        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            client = User.objects.get(user_id=client_id)
        except User.DoesNotExist:
            errors['client_id'] = ['Client does not exist']

        try:
            practitioner = User.objects.get(user_id=pract_id)
        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist']

        try:
            app_slot = AppointmentSlot.objects.get(id=slot_id)

            admin = User.objects.filter(company=company, user_type="Admin").first()

            # Check if there's already an appointment for the same date and time
            existing_appointment = GenericAppointment.objects.filter(
                slot=app_slot,
                appointment_time=slot_time,
                appointee=client,
                appointer=practitioner,
            ).first()

            if existing_appointment:
                errors['slot_date'] = ['Appointment for this date and time already exists.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)



            # Check for appointment interval
            _slot_date = app_slot.slot_date
            pract_interval = practitioner.availability_interval


            new_appointment = GenericAppointment.objects.create(
                appointer=practitioner,
                appointee=client,
                app_admin=admin,
                slot=app_slot,
                appointment_date=app_slot.slot_date,
                appointment_time=slot_time,
            )

            app_slot.state = "Partial"
            app_slot.save()

            slot_times = TimeSlot.objects.filter(appointment_slot=app_slot)

            for time in slot_times:
                if str(time.time) == str(slot_time):
                    print("################")
                    print("The time is in the database")
                    if time.occupied:
                        errors['slot_time'] = ['Slot time is already occupied.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
                    elif not time.occupied:
                        time.occupied = True
                        time.occupant = client
                        time.appointment_id = new_appointment.id
                        time.save()

            occupied_count = TimeSlot.objects.filter(appointment_slot=app_slot, occupied=True)

            if len(occupied_count) == app_slot.time_slot_count:
                app_slot.state = "Occupied"
                app_slot.save()

            # SEND CLIENT EMAIL
            client_subject = f"Yay! Your Appointment with {practitioner.full_name} is Confirmed 🎉"
            client_content = f"Hey {client.full_name},\nGuess what? Your appointment with {practitioner.full_name} on {new_appointment.appointment_date} at {new_appointment.appointment_time} is all set! 🌟\n\nMark your calendar and set your reminders because we can't wait to see you!\n\nCheers,\n\nThe {company.company_name} Team"
            client_email = EmailMessage(
                client_subject,
                client_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[client.email]
            )
            client_email.send()
            # SEND PRACTITIONER EMAIL
            pract_subject = f"New Appointment Alert!🚨"
            pract_content = f"Hello {practitioner.full_name},\n\nGreat news! {client.full_name} has booked an appointment with you on {new_appointment.appointment_date} at {new_appointment.appointment_time}. Time to show off your skills!🌟\n\nBest,\n\nThe {company.company_name} Team"
            pract_email = EmailMessage(
                pract_subject,
                pract_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[practitioner.email]
            )
            pract_email.send()
            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=new_appointment.app_admin,
                subject="New Appointment Set",
                body=f"New appointment set between {practitioner.full_name} and {client.full_name} on {new_appointment.appointment_date} at {new_appointment.appointment_time}"
            )
            new_activity.save()

            data['appointment_id'] = new_appointment.appointment_id
            payload['data'] = data

        except AppointmentSlot.DoesNotExist:
            errors['slot_id'] = ['Slot does not exist']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment added successfully"
        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_appointment_view2222(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        slot_id = request.data.get('slot_id', "")
        slot_time = request.data.get('slot_time', "")


        if not client_id:
            errors['client_id'] = ['Client User ID is required.']

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot id is required.']

        if not slot_time:
            errors['slot_time'] = ['Slot time is required.']


        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            client = User.objects.get(user_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist']

        try:
            practitioner = User.objects.get(user_id=pract_id)
        except:
            errors['pract_id'] = ['Practitioner does not exist']

        try:
            app_slot = AppointmentSlot.objects.get(id=slot_id)

            admin = User.objects.filter(company=company, user_type="Admin").first()

            # Check if there's already an appointment for the same date and time
            existing_appointment = GenericAppointment.objects.filter(
                slot=app_slot,
                appointment_time=slot_time,
                appointee=client,
                appointer=practitioner,
            ).first()

            if existing_appointment:
                errors['slot_date'] = ['Appointment for this date and time already exists.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            new_appointment = GenericAppointment.objects.create(
                appointer=practitioner,
                appointee=client,
                app_admin=admin,
                slot=app_slot,
                appointment_date=app_slot.slot_date,
                appointment_time=slot_time,
            )

            app_slot.state = "Partial"
            app_slot.save()

            slot_times = TimeSlot.objects.filter(appointment_slot=app_slot)

            for time in slot_times:
                if str(time.time) == str(slot_time):
                    print("################")
                    print("The time is in database")
                    if time.occupied:
                        errors['slot_time'] = ['Slot time is already occupied.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
                    elif not time.occupied:
                        time.occupied = True
                        time.occupant = client
                        time.appointment_id = new_appointment.id
                        time.save()

            occupied_count = TimeSlot.objects.filter(appointment_slot=app_slot, occupied=True)

            if len(occupied_count) == app_slot.time_slot_count:
                app_slot.state = "Occupied"
                app_slot.save()

            # SEND CLIENT EMAIL
            client_subject = f"Yay! Your Appointment with {practitioner.full_name} is Confirmed 🎉"
            client_content = f"Hey {client.full_name},\nGuess what? Your appointment with {practitioner.full_name} on {new_appointment.appointment_date} at {new_appointment.appointment_time} is all set! 🌟\n\nMark your calendar and set your reminders because we can't wait to see you!\n\nCheers,\n\nThe {company.company_name} Team"
            client_email = EmailMessage(
                client_subject,
                client_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[client.email]
            )
            client_email.send()
            # SEND PRACTITIONER EMAIL
            pract_subject = f"New Appointment Alert!🚨"
            pract_content = f"Hello {practitioner.full_name},\n\nGreat news! {client.full_name} has booked an appointment with you on {new_appointment.appointment_date} at {new_appointment.appointment_time}. Time to show off your skills!🌟\n\nBest,\n\nThe {company.company_name} Team"
            pract_email = EmailMessage(
                pract_subject,
                pract_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[practitioner.email]
            )
            pract_email.send()
            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=new_appointment.app_admin,
                subject="New Appointment Set",
                body=f"New appointment set between {practitioner.full_name} and {client.full_name} on {new_appointment.appointment_date} at {new_appointment.appointment_time}"
            )
            new_activity.save()

            data['appointment_id'] = new_appointment.appointment_id
            payload['data'] = data

        except:
            errors['slot_id'] = ['Slot does not exist']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment added successfully"

        return Response(payload)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def update_appointment_view(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':

        client_id = request.data.get('client_id', "")

        company_id = request.data.get('company_id', "")
        appointment_id = request.data.get('appointment_id', "")
        slot_id = request.data.get('slot_id', "")
        old_slot_time = request.data.get('old_slot_time', "")
        new_slot_time = request.data.get('new_slot_time', "")

        if not client_id:
            errors['client_id'] = ['Client User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']
        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not old_slot_time:
            errors['old_slot_time'] = ['Old slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(old_slot_time) < 8:
                old_slot_time += ':00'

        if not new_slot_time:
            errors['new_slot_time'] = ['New slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(new_slot_time) < 8:
                new_slot_time += ':00'

        if not appointment_id:
            errors['appointment_id'] = ['Appointment Id is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            client = User.objects.get(user_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist']

        try:
            app_slot = AppointmentSlot.objects.get(id=slot_id)

            try:
                appointment = GenericAppointment.objects.get(appointment_id=appointment_id)
            except:
                errors['appointment_id'] = ['Appointment does not exist']

            slot_times = TimeSlot.objects.all().filter(appointment_slot=app_slot)

            appointment.appointment_time = new_slot_time
            appointment.save()

            for time in slot_times:

                if str(time.time) == str(old_slot_time):
                    time.appointment = None
                    time.occupied = False
                    time.occupant = None
                    time.save()

                if str(time.time) == str(new_slot_time):
                    time.appointment = appointment
                    time.occupied = True
                    time.occupant = client
                    time.save()

            appointment.status = "Pending"
            appointment.re_scheduled = True
            appointment.appointment_rescheduled_at = timezone.now()
            appointment.save()

            ### SEND CLIENT EMAIL ####
            client_subject = f"Appointment Rescheduled! New Time, Same Great Service 🕐"
            client_content = f"Hey {appointment.appointee.full_name},\n\nour appointment with {appointment.appointer.full_name} has been rescheduled to {appointment.appointment_date} at {appointment.appointment_time}. We're still super excited to see you!\n\nCheers,\n\nThe {company.company_name} Team"

            client_email = EmailMessage(
                client_subject,
                client_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[appointment.appointee.email])

            client_email.send()

            ### SEND PRACTITIONER EMAIL ####
            pact_subject = f"Appointment Rescheduled!🕐"
            pract_content = f"We want to inform you that the appointment for {appointment.appointee.full_name} has been rescheduled to {appointment.appointment_date} at {appointment.appointment_time}. Please make note of this change in your schedule.\n\nCheers,\n\nThe {company.company_name} Team"

            pract_email = EmailMessage(
                pact_subject,
                pract_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[appointment.appointer.email])

            pract_email.send()

            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=appointment.app_admin,
                subject="Appointment Rescheduled!",
                body=f"Appointment between {appointment.appointer.full_name} and {appointment.appointee.full_name} on {appointment.appointment_date} at {appointment.appointment_time} has been rescheduled."
            )
            new_activity.save()

        except:
            errors['slot_id'] = ['Slot does not exist']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment rescheduled successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def approve_appointment_view(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        company_id = request.data.get('company_id', "")
        appointment_id = request.data.get('appointment_id', "")



        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not appointment_id:
            errors['appointment_id'] = ['Appointment ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointment = GenericAppointment.objects.get(appointment_id=appointment_id)

            appointment.status = "Approved"
            appointment.re_scheduled = False
            appointment.appointment_approved_at = timezone.now()
            appointment.save()

            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=appointment.app_admin,
                subject="Appointment Approved",
                body=f"Appointment between {appointment.appointer.full_name} and {appointment.appointee.full_name} on {appointment.appointment_date} at {appointment.appointment_time} has been approved."
            )
            new_activity.save()

        except:
            errors['appointment_id'] = ['Appointment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment approved successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def decline_appointment_view(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        company_id = request.data.get('company_id', "")
        appointment_id = request.data.get('appointment_id', "")



        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not appointment_id:
            errors['appointment_id'] = ['Appointment ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointment = GenericAppointment.objects.get(appointment_id=appointment_id)

            print(appointment)
            time_slots_data = TimeSlot.objects.all().filter(appointment_id=appointment.id).first()
            print(time_slots_data)
            time_slots_data.appointment = None
            time_slots_data.occupied = False
            time_slots_data.occupant = None
            time_slots_data.save()
#
            appointment.status = "Declined"
            appointment.appointment_declined_at = timezone.now()
            appointment.save()
#
            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=appointment.app_admin,
                subject="Appointment Declined",
                body=f"Appointment between {appointment.appointer.full_name} and {appointment.appointee.full_name} on {appointment.appointment_date} at {appointment.appointment_time} has been declined."
            )
            new_activity.save()

            payload['message'] = "Appointment declined successfully"
            payload['data'] = data

        except:
            errors['appointment_id'] = ['Appointment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def start_appointment_view(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        company_id = request.data.get('company_id', "")
        appointment_id = request.data.get('appointment_id', "")



        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not appointment_id:
            errors['appointment_id'] = ['Appointment ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointment = GenericAppointment.objects.get(appointment_id=appointment_id)

            appointment.status = "Started"
           # appointment.re_scheduled = False
            appointment.appointment_start = timezone.now()
            appointment.save()

            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=appointment.app_admin,
                subject="Appointment Started",
                body=f"Appointment between {appointment.appointer.full_name} and {appointment.appointee.full_name} on {appointment.appointment_date} at {appointment.appointment_time} has started."
            )
            new_activity.save()

        except:
            errors['appointment_id'] = ['Appointment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment started successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_appointment_ongoing_view(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        company_id = request.data.get('company_id', "")
        appointment_id = request.data.get('appointment_id', "")


        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not appointment_id:
            errors['appointment_id'] = ['Appointment ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointment = GenericAppointment.objects.get(appointment_id=appointment_id)

            appointment.status = "Ongoing"
           # appointment.re_scheduled = False
            appointment.save()

            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=appointment.app_admin,
                subject="Appointment Ongoing",
                body=f"Appointment between {appointment.appointer.full_name} and {appointment.appointee.full_name} on {appointment.appointment_date} at {appointment.appointment_time} is ongoing."
            )
            new_activity.save()

        except:
            errors['appointment_id'] = ['Appointment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment set to ongoing successfully"
        payload['data'] = data

        return Response(payload)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def complete_appointment_view(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        company_id = request.data.get('company_id', "")
        appointment_id = request.data.get('appointment_id', "")


        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not appointment_id:
            errors['appointment_id'] = ['Appointment ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointment = GenericAppointment.objects.get(appointment_id=appointment_id)

            appointment.status = "Completed"
           # appointment.re_scheduled = False
            appointment.appointment_end = timezone.now()
            appointment.save()

            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=appointment.app_admin,
                subject="Appointment Completed",
                body=f"Appointment between {appointment.appointer.full_name} and {appointment.appointee.full_name} on {appointment.appointment_date} at {appointment.appointment_time} is complete."
            )
            new_activity.save()

        except:
            errors['appointment_id'] = ['Appointment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment completed successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def cancel_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        company_id = request.data.get('company_id', "")
        appointment_id = request.data.get('appointment_id', "")


        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        if not appointment_id:
            errors['appointment_id'] = ['Appointment ID is required.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment = GenericAppointment.objects.get(appointment_id=appointment_id)

            if appointment.status == "Canceled":
                payload['message'] = "Appointment is already canceled."
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            time_slot = TimeSlot.objects.all().filter(appointment_id=appointment.id).first()
            if time_slot:
                time_slot.appointment = None
                time_slot.occupied = False
                time_slot.occupant = None
                time_slot.save()

            appointment.status = "Canceled"
            appointment.appointment_cancelled_at = timezone.now()
            appointment.save()

            # SEND CLIENT EMAIL
            client_subject = f"Appointment Cancelled. We'll Miss You!😢"
            client_content = f"Hi {appointment.appointee.full_name},\n\nWe're sad to hear you've canceled your appointment with {appointment.appointer.full_name}. But hey, life happens! Feel free to book again whenever you're ready.\n\nTake care,\nThe {company.company_name} Team"

            client_email = EmailMessage(
                client_subject,
                client_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[appointment.appointee.email])

            client_email.send()

            # SEND PRACTITIONER EMAIL
            pract_subject = f"Change of Plans! Appointment Cancelled📅"
            pract_content = f"Hello {appointment.appointer.full_name},\n\nJust a heads-up, {appointment.appointee.full_name} has canceled their appointment on {appointment.appointment_date} at {appointment.appointment_time}. Don't worry, there are plenty more fish in the sea!🐠\n\nBest,\nThe {company.company_name} Team"

            pract_email = EmailMessage(
                pract_subject,
                pract_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[appointment.appointer.email])

            pract_email.send()

            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=appointment.app_admin,
                subject="Appointment Cancelled",
                body=f"{appointment.appointee.full_name} cancelled their appointment with {appointment.appointer.full_name} on {appointment.appointment_date} at {appointment.appointment_time}"
            )
            new_activity.save()

            payload['message'] = "Appointment cancelled successfully"
            payload['data'] = data

        except GenericAppointment.DoesNotExist:
            errors['appointment_id'] = ['Appointment does not exist.']
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    return Response(payload)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def list_practitioner_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        pract_id = request.data.get('pract_id', "")
        company_id = request.data.get('company_id', "")
        appointment_status = request.data.get('appointment_status', "")  # Add this line

        if not pract_id:
            errors['pract_id'] = ['Practitioner User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            practitioner = User.objects.get(user_id=pract_id)

            # Filter appointments based on status
            filters = {'appointer': practitioner}
            if appointment_status:
                filters['status'] = appointment_status

            all_pract_appointments = GenericAppointment.objects.filter(**filters).order_by('-created_at')

            all_pract_appointments_serializer = ListPractGenericAppointmentSerializer(all_pract_appointments, many=True)
            _all_pract_appointments = all_pract_appointments_serializer.data
            data['all_pract_appointments'] = _all_pract_appointments

        except User.DoesNotExist:
            errors['pract_id'] = ['Practitioner does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointments retrieved successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def list_practitioner_appointment_view222(request):
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
            practitioner = User.objects.get(user_id=pract_id)

            all_pract_appointments = GenericAppointment.objects.all().filter(appointer=practitioner).order_by(
                '-created_at')

            all_pract_appointments_serializer = ListPractGenericAppointmentSerializer(all_pract_appointments, many=True)
            if all_pract_appointments_serializer:
                _all_pract_appointments = all_pract_appointments_serializer.data
                data['all_pract_appointments'] = _all_pract_appointments

        except:
            errors['pract_id'] = ['Practitioner does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointments retrieved successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def list_client_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        company_id = request.data.get('company_id', "")
        appointment_status = request.data.get('appointment_status', "")  # Add this line

        if not client_id:
            errors['client_id'] = ['Client User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

        try:
            client = User.objects.get(user_id=client_id)

            # Filter appointments based on status
            filters = {'appointee': client}
            if appointment_status:
                filters['status'] = appointment_status

            all_client_appointments = GenericAppointment.objects.filter(**filters).order_by('-created_at')

            all_client_appointments_serializer = ListClientGenericAppointmentSerializer(all_client_appointments,
                                                                                        many=True)
            _all_client_appointments = all_client_appointments_serializer.data
            data['all_client_appointments'] = _all_client_appointments

        except User.DoesNotExist:
            errors['client_id'] = ['Client does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointments retrieved successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def list_client_appointment_view222(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':

        client_id = request.data.get('client_id', "")

        company_id = request.data.get('company_id', "")

        if not client_id:
            errors['client_id'] = ['Client User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']


        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            client = User.objects.get(user_id=client_id)

            all_client_appointments = GenericAppointment.objects.all().filter(appointee=client).order_by('-created_at')

            all_client_appointments_serializer = ListClientGenericAppointmentSerializer(all_client_appointments,
                                                                                        many=True)
            if all_client_appointments_serializer:
                _all_client_appointments = all_client_appointments_serializer.data
                data['all_client_appointments'] = _all_client_appointments

        except:
            errors['client_id'] = ['Client does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointments retrieved successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def appointment_detail_view(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':

        appointment_id = request.data.get('appointment_id', "")

        company_id = request.data.get('company_id', "")

        if not appointment_id:
            errors['appointment_id'] = ['Appointment ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']


        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            appointment = GenericAppointment.objects.get(appointment_id=appointment_id)
            appointment_detail_serializer = GenericAppointmentSerializer(appointment, many=False)
            if appointment_detail_serializer:
                _appointment_detail_serializer = appointment_detail_serializer.data
                data['appointment_detail'] = _appointment_detail_serializer
        except:
            errors['appointment_id'] = ['Appointment does not exist.']




        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointments retrieved successfully"
        payload['data'] = data

        return Response(payload)
