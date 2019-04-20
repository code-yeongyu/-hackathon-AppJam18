from django.db import models
from django.contrib.postgres.fields import JSONField
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from group.models import Group


class Image(models.Model):
    image = models.ImageField(upload_to='static/uploaded/images/%Y/%m/%d/', )
    thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(width=300)],
        format='JPEG',
        options={'quality': 60})


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(
        'auth.user', related_name='article_writer', on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, related_name='article_group', on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=True)
    images_id = JSONField(
        blank=False, null=False,
        default=list)  # 한 게시글 당 여러 이미지를 저장 하기 위한 JSONField사용

    def __str__(self):  # 본 클래스의 문자열 표현
        return self.content

    class Meta:
        ordering = ('created_at', )
