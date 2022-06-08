from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from registration.models import UserNeighborhood
from .models import (
    Post,
    Comment,
    Complaint,
)
from .forms import (
    PostForm,
    CommentForm,
)

@login_required
def posts(request):
    posts = Post.objects.all()
    args = {}
    found = False
    users_neighborhoods = UserNeighborhood.objects.all()
    if users_neighborhoods is not None:
        for user_neighborhood in users_neighborhoods:
            if user_neighborhood.user == request.user:
                found = True
                # return render(request, 'posts.html', {'posts': posts})
    if not found:
        args['error'] = "Para ingresar a esta sección, unite a un barrio de Rafaela!"
        # return render(request, 'base.html', {'args': args})
    return render(request, 'posts.html', {'posts': posts,
                                          'args': args})

@login_required
def addPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            forum_post = form.save(commit=False)
            forum_post.author = request.user
            forum_post.save()
            # redireccionar al detalle después: return redirect('forumpostdetail', pk=forum_post.pk)
            return redirect('forum:posts')
    else:
        # después del login redireccionar al for
        form = PostForm()
    return render(request, 'form.html', {'form': form})

@login_required
def postDetail(request, pk):
    post = Post.objects.get(pk = pk)
    comments = Comment.objects.filter(post = post).annotate(like_count=Count('likes')).order_by('-like_count')
    #ordenar las respuestas por cantidad de likes
    #Article.objects.annotate(like_count=Count('likes')).order_by('-like_count')
    #COMENTARIOS o sea RESPUESTAS
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    else:
        form = CommentForm()

    # ver si el usuario le puso o no like a la respuesta
    for comment in comments:
        comment.total = comment.likes.count()
        if comment.likes.filter(id=request.user.id).exists():
            comment.liked = True

    user_complaints = Complaint.objects.filter(user=request.user)

    reported_comments = []
    for complaint in user_complaints:
        comment = complaint.comentario
        reported_comments.append(comment)

    return render(
        request,
        'detail.html',
        {
            'post': post,
            'comments': comments,
            'complaints': reported_comments,
        }
    )

@login_required
def deletePost(request, pk):
    # pk del forum post
    post = Post.objects.get(pk = pk)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
