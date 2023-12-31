from django.urls import path

from slots.api.views import set_appointer_slot, list_practitioner_availability, update_appointer_slot, \
    remove_appointer_slot, set_availability_interval, set_recurring_slot, set_recurring_list_slot

app_name = 'slots'

urlpatterns = [
    path('set-availability/', set_appointer_slot, name="set_appointer_slot"),
    path('set-recurring-slot/', set_recurring_slot, name="set_recurring_slot"),
    path('set-recurring-list-slot/', set_recurring_list_slot, name="set_recurring_list_slot"),
    path('update-availability/', update_appointer_slot, name="update_appointer_slot"),
    path('remove-availability/', remove_appointer_slot, name="remove_appointer_slot"),
    path('list-practitioner-availability/', list_practitioner_availability, name="list_practitioner_availability"),

    path('set-availability-interval/', set_availability_interval, name="set_availability_interval")

]
