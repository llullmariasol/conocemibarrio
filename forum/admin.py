from django.contrib import admin

from forum.models import Complaint, Comment, Post, Notification

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Complaint)
admin.site.register(Notification)
