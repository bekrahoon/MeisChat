from rest_framework.serializers import ModelSerializer
from chat.models import GroupIs


class GroupIsSerializer(ModelSerializer):
    class Meta:
        model = GroupIs
        fields = '__all__'