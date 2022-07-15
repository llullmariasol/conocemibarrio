from django.urls import path
from .views import (
    addPost,
    posts,
    postDetail,
    deletePost,
    likeComment,
    deleteComment,
    reportComment,
)

app_name = 'forum'

urlpatterns = [
    path('', posts, name='posts'),
    path('new-topic/', addPost, name='addPost'),
    path('topic/<int:pk>/', postDetail, name='postDetail'),
    path('topic/<int:pk>/delete/', deletePost, name='deletePost'),
    path('like-comment/<int:pk>/', likeComment, name='likeComment'),
    path('comment/<int:pk>/delete/', deleteComment, name='deleteComment'),
    path('report-comment/<int:pk>/', reportComment, name='reportComment'),
]
