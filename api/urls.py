# urls.py
from django.urls import path
from movie.views import VideoViewSet
from users.views import RegisterView, LoginView, UserListView

video_list = VideoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
video_detail = VideoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('videos/', video_list, name='video-list'),
    path('videos/<int:pk>/', video_detail, name='video-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
]