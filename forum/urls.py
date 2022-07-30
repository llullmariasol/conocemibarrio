from django.urls import path
from django.views.generic import TemplateView

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
    path('topic/<int:pk>/sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
    path('topic/<int:pk>/delete/', deletePost, name='deletePost'),
    path('like-comment/<int:pk>/', likeComment, name='likeComment'),
    path('comment/<int:pk>/delete/', deleteComment, name='deleteComment'),
    path('report-comment/<int:pk>/', reportComment, name='reportComment'),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript'))

]
