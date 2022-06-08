from django.urls import path
from .views import (
    addPost,
    posts,
    postDetail,
    deletePost,
)

app_name = 'forum'

urlpatterns = [
    path('', posts, name='posts'),
    path('new-topic/', addPost, name='addPost'),
    path('topic/<int:pk>/', postDetail, name='postDetail'),
    path('topic/<int:pk>/delete/', deletePost, name='deletePost'),
]
