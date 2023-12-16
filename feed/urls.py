from django.urls import path
from rest_framework import routers

from feed.views import PostView, CommmentView, ActionView

router = routers.SimpleRouter()
router.register('comments', CommmentView)

urlpatterns = [
    path('post/', PostView.as_view()),
    path('post/<int:pk>/', PostView.as_view()),
    path('post/<int:post_id>/action/', ActionView.as_view()),
    path('post/<int:post_id>/action/<int:action_id>/', ActionView.as_view()),
]

urlpatterns += router.urls