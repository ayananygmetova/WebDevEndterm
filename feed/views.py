from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from feed.models import Post, Comment, Action
from feed.serializers import PostSerializer, CommentSerializer
from feed.validators import PostValidator, PostUpdateValidator, ActionValidator


class PostView(APIView):
    def get(self, request):
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            validator = PostValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            data = validator.validated_data
            new_post = Post.objects.create(author_id=data.get('author_id'),
                                           content=data.get('content'),
                                           fiel=data.get('file'))
            return Response(PostSerializer(new_post).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            validator = PostUpdateValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            data = validator.validated_data
            changed_post = Post.objects.get(id=pk)
            if data.get('content'):
                changed_post = data.get('content')
            if data.get('file'):
                changed_post = data.get('file')
            changed_post.save()
            return Response(PostSerializer(changed_post).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.filter(id=pk)
        if post:
            post.delete()
        return Response("OK", status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        try:
            post = Post.objects.filter(id=pk).first()
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CommmentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer()

    def post(self, request, post_id):
        queryset = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(queryset, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


class ActionView(APIView):
    def post(self, request, pk):
        try:
            validator = ActionValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            data = validator.validated_data
            Action.objects.create(user_id=request.user.id,
                                  post_id=data.get('post_id'),
                                  is_liked=data.get('is_liked'))
            return Response()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        likes = Action.objects.filter(post_id=post_id, is_liked=True).count()
        dislikes = Action.objects.filter(post_id=post_id, is_liked=False).count()
        return Response({'likes': likes, 'dislikes': dislikes})

    def delete(self, request, post_id, action_id):
        Action.objects.filter(id=action_id).delete()
        return Response(True, status=status.HTTP_200_OK)
