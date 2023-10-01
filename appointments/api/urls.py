from django.urls import path

from appointments.api.views import set_appointment_view, update_appointment_view, \
    cancel_appointment_view, approve_appointment_view, decline_appointment_view, start_appointment_view, \
    set_appointment_ongoing_view, complete_appointment_view, list_practitioner_appointment_view, \
    appointment_detail_view, list_client_appointment_view

app_name = 'appointments'

urlpatterns = [
    path('set-appointment/', set_appointment_view, name="set_appointment_view"),
    path('update-appointment/', update_appointment_view, name="update_appointment_view"),
    path('cancel-appointment/', cancel_appointment_view, name="cancel_appointment_view"),
    path('approve-appointment/', approve_appointment_view, name="approve_appointment_view"),
    path('decline-appointment/', decline_appointment_view, name="decline_appointment_view"),
    path('start-appointment/', start_appointment_view, name="start_appointment_view"),
    path('set-appointment-ongoing/', set_appointment_ongoing_view, name="set_appointment_ongoing_view"),
    path('complete-appointment/', complete_appointment_view, name="complete_appointment_view"),

    path('list-practitioner-appointments/', list_practitioner_appointment_view, name="list_practitioner_appointment_view"),
    path('list-client-appointments/', list_client_appointment_view, name="list_client_appointment_view"),
    path('appointment-detail/', appointment_detail_view, name="appointment_detail_view")

]
