from django.urls import path, include
from likes.views import LikeView

app_name = 'likes'

urlpatterns = [
    path("", LikeView.as_view()),
]
