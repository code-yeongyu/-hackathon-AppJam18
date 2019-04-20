import json
from urllib.parse import unquote

from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from articles.models import Article, Image
from articles.serializers import ArticleSerializer, ImageSerializer


class ArticleList(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    # 게시글 리스트 반환 제너릭 설정

    def _is_image_available(self, pk):
        try:
            Image.objects.get(id=pk)
            return True
        except Image.DoesNotExist:
            return False

    def post(self, request):  # 에러 테스트 필요함
        if request.user.is_authenticated and request.user.group != None:  # 사용자가 인증 되었을경우
            serializer = ArticleSerializer(data=request.data)
            for temp in json.loads(
                    request.data.get('images_id')):  # 이미지의 id값들이 유효한지 체크
                if not self._is_image_available(temp):  # 잘못된 id값을 받았을 경우
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            if serializer.is_valid():
                serializer.save(writer=request.user)  # 작성자 요청자로 설정
                return JsonResponse(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)  # 폼에 오류가 있을 경우
        return Response(status=status.HTTP_401_UNAUTHORIZED)  # 인증되지 않았을 경우

    def get(self, request):  # 에러 테스트 필요함
        if request.user.is_authenticated and request.user.group != None:  # 사용자가 인증 되었을경우
            return Response(Article.objects.filter(group=request.user.group))
        return Response(status=status.HTTP_400_BAD_REQUEST)  # 인증되지 않았을 경우


class ArticleDetail(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    # 게시글 받아오는 기능 제너릭 설정


@api_view(['POST'])
def create_image(request):
    if request.user.is_authenticated:
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "id": serializer.data['id']
                }, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

#base_dir 설정정
@api_view(['GET'])
def image(request, pk):  # 이미지 반환
    test_file = open(
        settings.BASE_DIR + "/" + str(
            get_object_or_404(Image, pk=pk).image.url), 'rb')
    return HttpResponse(
        content=test_file,
        content_type="image/jpeg",
        status=status.HTTP_200_OK)


@api_view(['GET'])
def image_thumbnail(request, pk):  # 이미지 반환

    test_file = open(
        unquote(settings.BASE_DIR + "/" +
                str(get_object_or_404(Image, pk=pk).thumbnail.url)), 'rb')
    return HttpResponse(
        content=test_file,
        content_type="image/jpeg",
        status=status.HTTP_200_OK)
