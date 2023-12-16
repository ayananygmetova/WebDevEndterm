from django.db import models

from auth_.models import User
from common.validators import validate_file_size, validate_extension


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    file = models.FileField(upload_to='content', validators=[validate_file_size, validate_extension], null=True,
                            blank=True)
    comments = models.ManyToManyField(Comment, null=True, blank=True, related_name='post')
    create_datetime = models.DateTimeField(auto_now_add=True)


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_liked = models.BooleanField(null=True, blank=True)

