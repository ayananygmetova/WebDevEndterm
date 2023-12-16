from rest_framework import serializers

from auth_.serializers import UserSerializer
from feed.models import Post


class CommentValidator(serializers.ModelSerializer):
    user = UserSerializer()
    create_datetime = serializers.DateTimeField(format="%d.%m.%Y, %H:%M:%S")

    class Meta:
        fields = ('user', 'text', 'create_datetim')


class PostValidator(serializers.ModelSerializer):
    create_datetime = serializers.DateTimeField(format="%d.%m.%Y, %H:%M:%S")
    author_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'author_id', 'content', 'file', 'create_datetime')


class PostUpdateValidator(serializers.Serializer):
    content = serializers.CharField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)
