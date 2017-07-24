from rest_framework import viewsets, permissions, status

from django.core import serializers
from django.http import JsonResponse, Http404
from django.db.models import Q

from user.serializers import BranchScheduleSerializer, BranchSerializer
from user.models import BranchSchedule, Branch, User

from datetime import datetime
import json
import pytz
import pprint
pp = pprint.PrettyPrinter(indent=4)


class BranchScheduleViewSet(viewsets.ModelViewSet):
    """
    API for branches schedule.
    """
    serializer_class = BranchScheduleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        success = False
        date_from = None
        date_to = None
        branch_schedules = None
        response = None

        branch_schedules_filter = BranchSchedule.objects

        if self.request.method == 'GET':
            branches = None
            if 'from' in self.request.GET and 'to' in self.request.GET:
                start = self.request.GET['from']
                end = self.request.GET['to']
                date_from = datetime.strptime(
                    start, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
                date_to = datetime.strptime(end, '%Y-%m-%d')
                date_to = date_to.replace(
                    hour=23, minute=59, second=59, microsecond=999)

            if 'branch' in self.request.GET:
                try:
                    branches = Branch.objects.get(
                        pk=self.request.GET['branch'])
                except Branch.DoesNotExist:
                    response = JsonResponse(
                        {'detail': 'Invalid Branch', 'success': success})
                    response.status = status.HTTP_400_BAD_REQUEST
                    return response

            if branches:
                branch_schedules = branch_schedules_filter.filter(
                    Q(branch=branches)).all()
            else:
                branch_schedules = branch_schedules_filter.all()

            if date_from and date_to:
                branch_schedules = branch_schedules_filter.filter(
                    date__range=[date_from, date_to])

            return branch_schedules.all().order_by('date')

    def list(self, request, *args, **kwargs):
        response = None
        queryset = self.get_queryset()
        serializer = BranchScheduleSerializer(queryset, many=True).data
        branch_schedules = json.dumps(serializer)
        response = JsonResponse(
            {'data': json.loads(branch_schedules), 'success': True})
        response.status = status.HTTP_200_OK
        return response

    def retrieve(self, request, pk=None):
        success = False
        response = None
        if pk:
            if request.user.user_type == User.ADMIN:
                try:
                    schedule_filter = Q(pk=pk) & Q(
                        status='OPEN') & Q(deleted__isnull=True)
                    queryset = BranchSchedule.objects.get(schedule_filter)
                    serializer = BranchScheduleSerializer(queryset).data
                    branches = json.dumps(serializer)
                    success = True
                    response = JsonResponse(
                        {'data': json.loads(branches), 'success': success})
                    response.status = status.HTTP_200_OK
                except Exception as e:
                    pp.pprint(e)
        else:
            response = JsonResponse(
                {'message': 'Invalid Request', 'success': success})
            response.status = status.HTTP_400_BAD_REQUEST

        return response

    def create(self, request):
        success = False
        response = None
        # b'{"day":"tue","date":"2017-07-11","status":"OPEN","start":"17:00:00","end":"20:30:00","branch":40}'
        req_field = ['day', 'status', 'start', 'end', 'date', 'branch']
        if (all(field in request.data for field in req_field)):
            date = datetime.strptime(
                request.data['date'], '%Y-%m-%d').replace(
                    hour=0,
                    minute=0,
                    second=0
                )
            start_time = datetime.strptime(
                request.data['start'], '%H:%M:%S').time()
            end_time = datetime.strptime(
                request.data['end'], '%H:%M:%S').time()

            # pp.pprint(str(date))
            # branch = Branch.objects.get(pk=request.data['branch'])
            # data = BranchSerializer(branch).data
            date = date.astimezone(pytz.utc)
            try:
                branch = Branch.objects.get(pk=request.data['branch'])
                branch_filter = Q(branch=branch) & Q(date=date) & Q(deleted__isnull=True)
                branch_query = BranchSchedule.objects.filter(
                    branch_filter).count()

                if branch_query == 0:
                    branch_schedule = BranchSchedule()
                    branch_schedule.date = date
                    branch_schedule.day = request.data['day']
                    branch_schedule.start = start_time
                    branch_schedule.end = end_time
                    branch_schedule.status = request.data['status']
                    # branch_schedule.account = request.account
                    branch_schedule.branch = branch
                    success = True
                    branch_schedule.save()
                    serializer = BranchScheduleSerializer(branch_schedule).data
                    branch_schedules = json.dumps(serializer)
                    response = JsonResponse(
                        {'data': json.loads(branch_schedules),
                         'success': success})
                    response.status = status.HTTP_201_CREATED
                else:
                    response = JsonResponse(
                        {'success': success,
                         'detail': 'Schedule already exists'})
                    response.status = status.HTTP_400_BAD_REQUEST

            except Branch.DoesNotExist:
                response = JsonResponse(
                    {'detail': 'Invalid Branch',
                     'success': success})
                response.status = status.HTTP_400_BAD_REQUEST
        else:
            response = JsonResponse(
                {'message': 'Invalid Request',
                 'success': success})
            response.status = status.HTTP_400_BAD_REQUEST

        return response

    def update(self, request, pk=None, *args, **kwargs):
        response = None
        success = False

        if pk:
            try:
                branch = Branch.objects.get(pk=request.data['branch'])
                branch_schedule = BranchSchedule.objects.get(
                    pk=pk, branch=branch)
                serializer = BranchScheduleSerializer(
                    branch_schedule, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    queryset = BranchScheduleSerializer(branch_schedule).data
                    branch_schedules = json.dumps(queryset)
                    response = JsonResponse(
                        {'data': json.loads(branch_schedules),
                         'success': success})
                    response.status = status.HTTP_200_OK

            except BranchSchedule.DoesNotExist:
                response = JsonResponse(
                    {'detail': 'Schedule does not exist',
                     'success': success})
                response.status = status.HTTP_400_BAD_REQUEST
        else:
            response = JsonResponse(
                {'detail': 'Invalid Request',
                 'success': success})

            response.status = status.HTTP_400_BAD_REQUEST

        return response

    def destroy(self, request, pk=None):
        success = False
        response = None

        try:
            branch = Branch.objects.get(pk=request.GET['branch'])
        except Branch.DoesNotExist:
            response = JsonResponse(
                {'success': success, 'detail': 'Invalid Branch'})
            response.status = status.HTTP_400_BAD_REQUEST

        if branch:
            try:
                branch_schedule = BranchSchedule.objects.get(
                    pk=pk, branch=branch)
                branch_schedule.delete()
                success = True
                response = JsonResponse(
                    {'success': True,
                     'message': 'Schedule successfully deleted'})
                response.status = status.HTTP_200_OK
            except BranchSchedule.DoesNotExist:
                response = JsonResponse(
                    {'detail': 'Schedule does not exist', 'success': success})
                response.status = status.HTTP_400_BAD_REQUEST

        return response
