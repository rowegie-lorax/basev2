from django.shortcuts import render
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from user.serializers import UserSerializer
from user.models import User
from . import EmailOrPhonenumberBackend
import pprint
pp = pprint.PrettyPrinter(indent=4)

validate = EmailOrPhonenumberBackend()

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


@api_view(['GET', 'POST'])
def login_user(request):
    username = request.POST['username'].strip()
    password = request.POST['password']
    success = False
    msg = None
    token = None
    user = validate.authenticate(username, password)
    if user is not None:
        if user.is_active:
            success = True
            msg = 'Successful Login'
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'success': success, 'token': token.key, 'data': UserSerializer(user).data},
                                status=status.HTTP_200_OK)
        else:
            msg = 'Account not verified, Please check email and verify account'
    else:
        msg = 'Invalid Credentials.'

    return JsonResponse({'success': success, 'message': msg}, status=status.HTTP_401_UNAUTHORIZED)


def user_login(request):
    username = request.POST['username'].strip()
    password = request.POST['password']
    success = False
    msg = None
    token = None
    user = validate.authenticate(username, password)
    if user is not None:
        if user.is_active:
            success = True
            msg = 'Successful Login'
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'success': success, 'token': token.key, 'data': UserSerializer(user).data},
                                status=status.HTTP_200_OK)
        else:
            msg = 'Account not verified, Please check email and verify account'
    else:
        msg = 'Invalid Credentials.'

    return JsonResponse({'success': success, 'message': msg}, status=status.HTTP_401_UNAUTHORIZED)


# def register(request):
#     email = request.POST['email'].strip()
#     phone = request.POST['phone_number']
#     password = request.POST['password']
#     user = User()
#     validate_email = User.objects.all().filter(email__iexact=email).count()
#     validate_phone = User.objects.all().filter(phone_number__iexact=phone).count()
#     serializer = UserSerializer(data={'email': email, 'phone_number': phone}) if validate_email is 0 and validate_phone is 0 else "Email or Phone already Exists!"
#     success = False
#     try:
#         if serializer.is_valid():
#             pp.pprint(serializer.data)
#             user.email = serializer.validated_data['email']
#             user.phone_number = serializer.validated_data['phone_number']
#             user.set_password(password)
#             success = True
#             user.save()
# return JsonResponse({'success': success },
# status=status.HTTP_201_CREATED)

#     except AttributeError as ex:
# return JsonResponse({'success': success, 'message': serializer},
# status=status.HTTP_400_BAD_REQUEST)
