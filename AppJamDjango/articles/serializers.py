from rest_framework import serializers
from articles.models import Article, Image


class ArticleSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    group = serializers.ReadOnlyField(source='writer.group')

    class Meta:
        model = Article
        fields = ('id', 'created_at', 'content',
                  'writer', 'group', 'images_id')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')
