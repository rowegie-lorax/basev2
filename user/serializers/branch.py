from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from user.models import Branch


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ('id', 'account', 'name', 'branch_alias',
                  'location', 'phone', 'create_at', 'update_at')
        validators = [
            UniqueTogetherValidator(
                queryset=Branch.objects.all(),
                fields=('name', 'account')
            )
        ]
