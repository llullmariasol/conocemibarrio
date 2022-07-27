from django.contrib import admin

from forum.models import Complaint, Comment, Post

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Complaint)
