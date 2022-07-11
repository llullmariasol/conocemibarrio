from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Post(models.Model):
    tittle = models.CharField(max_length=30)
    body = RichTextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # el related_name nos va a permitir acceder a los comentarios desde el post
    content = models.CharField(max_length=500)
    creationDate = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='forum_answers')
    complaints = models.ManyToManyField(User, related_name='complaints')
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def total_likes(self):
        return self.likes.count()

    def total_complaints(self):
        return self.complaints.count()

class Complaint(models.Model):
    REASONS = (
        (1, 'Contenido discriminativo'),
        (2, 'Comentario violento'),
        (3, 'Comentario de amenaza'),
        (4, 'Contenido irrespetuoso'),
        (5, 'Otro'),
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reported_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_who_reports')
    reason = models.CharField(choices=REASONS, default=1, max_length=30)
