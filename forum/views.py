from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from registration.models import UserNeighborhood
from .models import (
    Post,
    Comment,
    Complaint, Notification,
)
from .forms import (
    PostForm,
    CommentForm,
    ComplaintForm,
)


@login_required
def posts(request):
    try:
        user_neighborhood = UserNeighborhood.objects.get(user=request.user)
    except UserNeighborhood.DoesNotExist:
        return render(
            request,
            'join_a_neighborhood.html',
            {'function': "foro"}
        )
    post_list = Post.objects.all().filter(neighborhood=user_neighborhood.neighborhood)
    n = user_neighborhood.neighborhood.name
    return render(request, 'posts.html', {'posts': post_list, 'neighborhood': n})


@login_required
def addPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            user_neighborhood = UserNeighborhood.objects.all().filter(user=request.user).first()
            forum_post = form.save(commit=False)
            forum_post.author = request.user
            forum_post.neighborhood = user_neighborhood.neighborhood
            forum_post.save()
            return redirect('forum:posts')
    else:
        form = PostForm()
    return render(request, 'form.html', {'form': form})


@login_required
def postDetail(request, pk):
    post = Post.objects.get(pk=pk)
    author_user_id = post.author.pk
    comments = Comment.objects.filter(post=post).annotate(like_count=Count('likes')).order_by('-like_count')
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        for field in form:
            print("Field Error:", field.name,  field.errors)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    else:
        form = CommentForm()

    for comment in comments:
        comment.total = comment.likes.count()
        if comment.likes.filter(id=request.user.id).exists():
            comment.liked = True

    user_complaints = Complaint.objects.filter(user=request.user)

    reported_comments = []
    for complaint in user_complaints:
        comment = complaint.comment
        reported_comments.append(comment)

    return render(
        request,
        'detail.html',
        {
            'post': post,
            'form': form,
            'comments': comments,
            'complaints': reported_comments,
            'author_user_id': author_user_id,
        }
    )


@login_required
def deletePost(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def likeComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('forum:postDetail', args=[str(comment.post.id)]))


@login_required
def deleteComment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def reportComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(data=request.POST)
        complaint = Complaint()
        if form.is_valid:
            comment.complaints.add(request.user)
            if comment.total_complaints() > 4:
                comment.removed = True
            complaint.comment = comment
            complaint.user = request.user
            complaint.save()
            return HttpResponseRedirect(reverse('forum:postDetail', args=[str(comment.post.id)]))
    else:
        form = ComplaintForm()
    return render(
        request,
        'report.html',
        {
            'form': form,
            'comment': comment,
        },
    )


def notifications(request):
    notifications_list = Notification.objects.filter(recipient=request.user).order_by('creationDate').reverse()
    return render(request, 'notification_list.html', {'notifications': notifications_list})
