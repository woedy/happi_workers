from django.urls import path

from accounts.api.views import register_company, register_user, list_user_privileges, get_user_data

app_name = 'accounts'

urlpatterns = [
    path('register-company/', register_company, name="register_company"),

    path('register-user/', register_user, name="register_user"),
    path('list-user-privileges/', list_user_privileges, name="list_user_privileges"),

    path('get-user-data/', get_user_data, name="get_user_data"),
]
