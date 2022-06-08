from django import forms
from .models import (
    Post,
    Comment,
    Complaint,
)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

class ComplaintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args,**kwargs)

    class Meta:
        model = Complaint
        fields = ['reason',]
