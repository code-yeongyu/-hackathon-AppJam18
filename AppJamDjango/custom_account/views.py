from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from custom_account.forms import SignUpForm
from custom_account.models import Profile
from custom_account.serializers import ProfileSerializer


class ProfileOverall(APIView):  # 자신의 프로필 수정
    def get(self, request):  # 프로필 조회
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
            except:
                Profile.objects.create(user=request.user)
                profile = Profile.objects.get(user=request.user)
            return Response(
                {
                    "name": profile.nickname,
                    "group": profile.group.name
                },
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProfileDetail(APIView):  # 테스트 필요
    def get(self, request, string):  # 프로필 조회
        try:
            user = User.objects.get(username=string)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            profile = Profile.objects.get(user=user)
        except:
            Profile.objects.create(user=user)
            profile = Profile.objects.get(user=user)
        return Response(
            {
                "name": profile.nickname,
                "group": profile.group.name
            },
            status=status.HTTP_200_OK)


@api_view(['POST'])
def sign_up(request):  # 회원가입
    form = SignUpForm(request.POST)
    try:
        User.objects.get(email=request.POST['email'])
        return Response(
            {
                "email": "해당 이메일은 이미 존재합니다."
            },
            status=status.HTTP_406_NOT_ACCEPTABLE)
    except User.DoesNotExist:  # 이메일이 중복이 아닐경우에
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Profile.objects.create(user=user)
            Token.objects.create(user=user)
            return Response(status=status.HTTP_201_CREATED)
    except:
        return Response("please fill the email, username, password1, password2", status=status.HTTP_400_BAD_REQUEST)
    return Response(form.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def change_username(request):
    if request.user.is_authenticated:
        try:
            newusername = request.POST['nickname']
            if Profile.objects.filter(nickname=newusername).exists():
                return Response({"nickname": "해당 사용자 이름은 이미 존재합니다."})
            request.user.nickname = newusername
            profile = Profile.objects.get(user=request.user)
            profile.nickname = newusername
            profile.save()
            return Response(status=status.HTTP_200_OK)
        except:
            pass
    return Response(status=status.HTTP_400_BAD_REQUEST)
