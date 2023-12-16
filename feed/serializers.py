from rest_framework import serializers

from auth_.serializers import UserSerializer
from feed.models import Post


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    create_datetime = serializers.DateTimeField(format="%d.%m.%Y, %H:%M:%S")

    class Meta:
        fields = ('user', 'text', 'create_datetime')


class PostSerializer(serializers.ModelSerializer):
    create_datetime = serializers.DateTimeField(format="%d.%m.%Y, %H:%M:%S")
    author = UserSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'file', 'comments', 'create_datetime')


