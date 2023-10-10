import re

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from accounts.api.serializers import AppointerPrivilegeSerializer, HumanResourcesPrivilegeSerializer, \
    AdminPrivilegeSerializer, AppointeePrivilegeSerializer
from accounts.models import Company
from activities.models import AllActivity
from privileges.models import AdminPrivilege, AppointerPrivilege, HumanResourcesPrivilege, ClientPrivilege, \
    AppointeePrivilege

User = get_user_model()


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def register_company(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':
        company_name = request.data.get('company_name', "")

        admin_name = request.data.get('admin_name', "")
        admin_email = request.data.get('admin_email', '').lower()
        admin_phone = request.data.get('admin_phone', "")
        location = request.data.get('location', "")

        print(company_name)
        print(admin_name)
        print(admin_email)
        print(location)

        if not company_name:
            errors['company_name'] = ['Company name is required.']


        if not location:
            errors['location'] = ['Company location is required.']

        if not admin_email:
            errors['admin_email'] = ['Admin Email is required.']

        if not is_valid_email(admin_email):
            errors['admin_email'] = ['Valid email required.']



        if not admin_name:
            errors['admin_name'] = ['Admin name is required.']

        if not admin_phone:
            errors['admin_phone'] = ['Admin phone is required.']


        try:

            if check_email_exist(admin_email):
                errors['admin_email'] = ['Admin Email already exists in our database.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            # Create New Company Object
            new_company = Company.objects.create(
                company_name=company_name,
                company_phone=admin_phone,
                company_location=location,
            )

            # Add Company Admin
            new_admin = User.objects.create(
                email=admin_email,
                full_name=admin_name,
                company=new_company,
                phone=admin_phone,
                user_type="Admin"
            )

            try:
                token = Token.objects.get(user=new_admin)
            except Token.DoesNotExist:
                token = Token.objects.create(user=new_admin)
                #
                # Create Admin privileges
            new_priv = AdminPrivilege.objects.create(
                user_id=new_admin,
            )
            #
            # Add new ACTIVITY
            new_activity = AllActivity.objects.create(
                user=new_admin,
                subject="Company Added",
                body=new_admin.email + " Just added a new company."
            )
            new_activity.save()

            # SEND EMAIL TO ADMIN/COMPANY for joining the platform.
            ##
            ##
            ##
            ##
            ##
            #
            data['company_name'] = new_company.company_name
            data['company_id'] = new_company.company_id
            #
            data['admin_full_name'] = new_admin.full_name
            data['admin_user_id'] = new_admin.user_id
            data["admin_token"] = token.key

            payload['message'] = "Successful"
            payload['data'] = data


        except IntegrityError:
            errors['admin_email'] = ['Admin Email already exists in our database.']
#
#


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Successful"
        payload['data'] = data




    return Response(payload)


def check_email_exist(email):

    qs = User.objects.filter(email=email)
    if qs.exists():
        return True
    else:
        return False


def is_valid_email(email):
    # Regular expression pattern for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Using re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False




@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def register_user(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email = request.data.get('email', "").lower()
        full_name = request.data.get('full_name', "")
        user_type = request.data.get('user_type', "")
        company_id = request.data.get('company_id', "")
        time_zone = request.data.get('time_zone', "")

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']
        elif check_email_exist(email):
            errors['email'] = ['Email already exists in our database.']

        if not full_name:
            errors['full_name'] = ['Full Name is required.']
        if not user_type:
            errors['user_type'] = ['User type is required.']
        if not time_zone:
            errors['time_zone'] = ['User timezone is required.']
        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)

            try:
                new_user = User.objects.create(
                    email=email,
                    full_name=full_name,
                    company=company,
                    user_type=user_type,
                    time_zone=time_zone
                )
                try:
                    token = Token.objects.get(user=new_user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=new_user)

                # Check user type and assign the right Privilege
                appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']
                if user_type in appointer_list:
                    new_priv = AppointerPrivilege.objects.create(user_id=new_user)
                elif user_type == "HR":
                    new_priv = HumanResourcesPrivilege.objects.create(user_id=new_user)
                elif user_type == "Admin":
                    new_priv = AdminPrivilege.objects.create(user_id=new_user)
                elif user_type == "Client":
                    new_priv = AppointeePrivilege.objects.create(user_id=new_user)

                data['full_name'] = new_user.full_name
                data['user_id'] = new_user.user_id
                data['user_type'] = new_user.user_type
                data["token"] = token.key
                data['company_name'] = company.company_name
                data['company_id'] = company.company_id

                # Add new ACTIVITY
                new_activity = AllActivity.objects.create(
                    user=User.objects.get(id=1),
                    subject="New user registered",
                    body=f"{company.company_name} just registered {new_user.full_name} as a new user."
                )
                new_activity.save()
            except IntegrityError:
                errors['email'] = ['Email already exists in our database.']

        except Company.DoesNotExist:
            errors['company_id'] = ['Company does not exist.']

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
def list_user_privileges(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        user_id = request.data.get('user_id', "")
        company_id = request.data.get('company_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        if not company_id:
            errors['company_id'] = ['Company ID is required.']

        try:
            company = Company.objects.get(company_id=company_id)
        except:
            errors['company_id'] = ['Company does not exist.']

        try:
            user = User.objects.get(user_id=user_id)

            appointer_list = ['Practitioner', 'Doctor', 'Teacher', 'Interviewer']

            if user.user_type in appointer_list:
                privileges = AppointerPrivilege.objects.all().filter(user_id=user).first()
                all_privilege_serializer = AppointerPrivilegeSerializer(privileges, many=False)
                if all_privilege_serializer:
                    _all_privileges = all_privilege_serializer.data
                    data['user_privilege'] = _all_privileges

            elif user.user_type == "HR":
                privileges = HumanResourcesPrivilege.objects.all().filter(user_id=user).first()
                all_privilege_serializer = HumanResourcesPrivilegeSerializer(privileges, many=False)
                if all_privilege_serializer:
                    _all_privileges = all_privilege_serializer.data
                    data['user_privilege'] = _all_privileges

            elif user.user_type == "Admin":
                privileges = HumanResourcesPrivilege.objects.all().filter(user_id=user).first()
                all_privilege_serializer = AdminPrivilegeSerializer(privileges, many=False)
                if all_privilege_serializer:
                    _all_privileges = all_privilege_serializer.data
                    data['user_privilege'] = _all_privileges
            elif user.user_type == "Client":
                privileges = AppointeePrivilege.objects.all().filter(user_id=user).first()
                all_privilege_serializer = AppointeePrivilegeSerializer(privileges, many=False)
                if all_privilege_serializer:
                    _all_privileges = all_privilege_serializer.data
                    data['user_privilege'] = _all_privileges
        except:
            errors['user_id'] = ['User does not exist.']


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


