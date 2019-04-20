import rest_framework.status
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from custom_account.serializers import ProfileSerializer
from group.models import Group as GroupModel
from custom_account.models import Profile


class Group(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(request.user.group.group_id)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            new_group = GroupModel(
                name=request.data.get('name'), admin=request.user)
            new_group.save()
            return Response(new_group.group_id, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def join_group(request, pk):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            profile.group = GroupModel.objects.get(group_id=pk)
            profile.group.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
