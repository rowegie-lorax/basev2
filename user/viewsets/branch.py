from rest_framework import viewsets, permissions, status

from django.http import JsonResponse
from django.db.models import Q

from user.permissions import IsOwnerOrReadOnly
from user.serializers import BranchSerializer
from user.models import Branch
from user.models import User

import json


class BranchViewSet(viewsets.ModelViewSet):
    """
    API for branches.
    """
    serializer_class = BranchSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Branch.objects.filter(
            deleted__isnull=True, account=self.request.user.account).all()
        return queryset

    def list(self, request):
        success = False
        response = None
        try:
            if request.user.user_type == User.ADMIN:
                branch_filter = Q(deleted__isnull=True) & Q(
                    account=self.request.user.account)
                queryset = Branch.objects.filter(branch_filter).all()
                serializer = BranchSerializer(queryset, many=True)
                branches = json.dumps(serializer.data)
                success = True
                response = JsonResponse(
                    {'data': json.loads(branches), 'success': success})
                response.status = status.HTTP_200_OK
        except:
            response = JsonResponse(
                {'success': success, 'detail': 'Invalid Request'})
            response.status = status.HTTP_401_UNAUTHORIZED

        return response

    def retrieve(self, request, pk=None):
        success = False
        response = None
        if pk:
            if request.user.user_type == User.ADMIN:
                try:
                    branch_filter = Q(pk=pk) & Q(deleted__isnull=True) & Q(
                        account=self.request.user.account)
                    queryset = Branch.objects.get(branch_filter)
                    serializer = BranchSerializer(queryset).data
                    branches = json.dumps(serializer)
                    success = True
                    response = JsonResponse(
                        {'data': json.loads(branches), 'success': success})
                    response.status = status.HTTP_200_OK
                except:
                    response = (
                        {'detail': 'Branch does not exist',
                         'success': success})
                    response.status = status.HTTP_400_BAD_REQUEST
        else:
            response = ({'detail': 'Invalid Request',
                         'success': success})
            response.status = status.HTTP_400_BAD_REQUEST

        return response

    def create(self, request, *args, **kwargs):
        success = False
        response = None

        name_count = Branch.objects.filter(
            name__iexact=request.data['name']).count()

        if name_count == 0:
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True

            request.data['account'] = request.user.account.pk
            request.data['branch_alias'] = request.data['name']

            if request.user.user_type == User.ADMIN:
                serializer = BranchSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                success = True
                response = JsonResponse(
                    {'data': serializer.data,
                     'success': success})
                response.status = status.HTTP_201_CREATED
        else:
            response = JsonResponse(
                {'message': 'Branch name already exits!',
                 'success': success})
            response.status = status.HTTP_400_BAD_REQUEST

        return response

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)

    def update(self, request, pk=None, *args, **kwargs):
        response = None
        success = False

        branch_count = Branch.objects.filter(
            name__iexact=request.data['name']).count()
        if branch_count == 0:
            if pk:
                try:
                    branch = Branch.objects.get(pk=pk)
                    if hasattr(request.data, '_mutable'):
                        request.data._mutable = True

                    request.data['account'] = request.user.account.pk
                    request.data['branch_alias'] = request.data['name']

                    if request.user.user_type == User.ADMIN:
                        return super().update(request, pk, *args, **kwargs)
                except:
                    response = JsonResponse(
                        {'message': 'Branch does not exist',
                         'success': success})
                    response.status = status.HTTP_400_BAD_REQUEST
        else:
            response = JsonResponse(
                {'message': 'Branch name already exits!',
                 'success': success})

            response.status = status.HTTP_400_BAD_REQUEST

        return response

    def destroy(self, request, pk=None):
        success = False
        response = None
        if pk:
            if request.user.user_type == User.ADMIN:
                branch = Branch.objects.get(pk=pk)
                branch.delete()
                success = True
                response = JsonResponse(
                    {'success': success,
                     'message': 'Branch successfully deleted'})
                response.status = status.HTTP_200_OK
            else:
                response = JsonResponse(
                    {'success': success,
                     'message': 'Not allowed to delete branch'})
                response.status = status.HTTP_401_UNAUTHORIZED
        else:
            response = JsonResponse(
                {'success': success,
                 'message': 'Invalid request'})
            response.status = status.HTTP_400_BAD_REQUEST

        return response
