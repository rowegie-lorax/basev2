from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from django.db.models import Q

from user.serializers import UserSerializer
from user.models import User
from user.forms import RegistrationForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        response = None
        success = False

        if request.user.is_authenticated():
            user_filter = Q(is_admin=False) & Q(deleted__isnull=True)
            queryset = User.objects.all().filter(user_filter)
            serializer = UserSerializer(queryset, many=True)
            success = True
            response = JsonResponse(
                {'data': serializer.data,
                 'success': success},
                safe=False)
            response.status = status.HTTP_200_OK
        else:
            response = JsonResponse(
                {'message': 'Invalid Request',
                 'success': False})
            response.status = status.HTTP_401_UNAUTHORIZED

        return response

    def retrieve(self, request, pk=None):
        success = False

        if request.user.is_authenticated():
            try:
                user = User.objects.filter(is_admin=False).get(pk=pk)
                user = UserSerializer(user).data
                success = True
                response = JsonResponse(
                    {'success': success,
                     'data': user})
                response.status = status.HTTP_200_OK
            except User.DoesNotExist:
                response = JsonResponse(
                    {'success': success,
                     'detail': 'User does not exist'})
                response.status = status.HTTP_400_BAD_REQUEST
        else:
            response = JsonResponse(
                {'success': success,
                 'detail': 'Not Authorized'})
            response.status = status.HTTP_401_UNAUTHORIZED

        return response

    def create(self, request):
        success = False
        response = None

        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                phone_number=form.cleaned_data['phone_number'],
                user_type=request.data['user_type'])
            # user.phone_number =
            # email side
            password = form.cleaned_data['password']
            user.set_password(password)
            success = True
            user.save()
            response = JsonResponse(
                {'success': success,
                 'detail': 'User successfully created'})
            response.status = status.HTTP_201_CREATED
        else:
            response = JsonResponse(
                {'success': success, 'detail': form.errors})
            response.status = status.HTTP_400_BAD_REQUEST

        return response

    def update(self, request, pk=None):
        response = None
        success = False
        msg = ''

        if request.user.is_authenticated():
            try:
                user = User.objects.get(pk=pk)
                user.email = request.data['email']
                user.phone_number = request.data['phone_number']
                user.user_type = request.data['user_type']
                if ('password' in request.data):
                    user.set_password(request.data['password'])
                user.save()
                msg = 'User successfully updated!'

                response = JsonResponse(
                    {'success': success,
                     'detail': msg,
                     'data': UserSerializer(user).data})
                response.status = status.HTTP_200_OK

            except User.DoesNotExist:
                msg = 'User does not exist!'
                response = JsonResponse(
                    {'success': success,
                     'detail': msg})
                response.status = status.HTTP_400_BAD_REQUEST
        else:
            msg = 'Not Authorized!'
            response = JsonResponse(
                {'success': success,
                 'detail': msg}),
            response.status = status.HTTP_401_UNAUTHORIZED

        return response

    def destroy(self, request, pk=None):
        response = None
        success = False
        if request.user.is_authenticated():
            try:
                user = User.objects.get(pk=pk)
                user.delete()
                success = True
                response = JsonResponse(
                    {'success': success,
                     'message': 'User successfully deleted'})
                response.status = status.HTTP_200_OK

            except User.DoesNotExist:
                response = JsonResponse(
                    {'success': success,
                     'detail': 'User does not exist'})
                response.status = status.HTTP_400_BAD_REQUEST
        else:
            response = JsonResponse({'detail': 'UInvalid Request'})
            response.status = status.HTTP_401_UNAUTHORIZED

        return response
