from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat.models import GroupIs
from .serializers import GroupIsSerializer
from chat.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/groups',
        'GET /api/groups/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getGroups(request):
    groups = GroupIs.objects.all()
    serializer = GroupIsSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getGroup(request, pk):
    group = GroupIs.objects.get(id=pk)
    serializer = GroupIsSerializer(group, many=False)
    return Response(serializer.data)