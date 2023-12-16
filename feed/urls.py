from django.urls import path

from feed.views import PostView

urlpatterns = [
    path('post/', PostView.as_view()),
    path('post/<int:pk>/', PostView.as_view())
]
