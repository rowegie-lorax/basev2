from rest_framework import serializers
from user.models import BranchSchedule


class BranchScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchSchedule
        fields = ('id', 'branch', 'day', 'status', 'start', 'end',
                  'date', 'create_at', 'update_at')
