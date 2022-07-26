import logging
import requests
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from registration.models import UserNeighborhood
from .models import (
    Post,
    Comment,
    Complaint,
)
from .forms import (
    PostForm,
    CommentForm,
    ComplaintForm,
)

# logger = logging.getLogger('app_api')


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
    if request.method == "POST":
        # token = request.POST.get('token')
        # sendNotification([token], "CONOCE MI BARRIO", "El usuario " + request.user.username + "comentó tu foro")
        # send_push(request)
        form = CommentForm(data=request.POST)
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
            if comment.complaints > 4:
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


# def showFirebaseJS(request):
#     data = 'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
#          'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
#          'var firebaseConfig = {' \
#          '        apiKey: "AIzaSyBdGZanwe4TlpxENzBV8EuUoRxgClGf",' \
#          '        authDomain: "conocemibarrio.firebaseapp.com",' \
#          '        projectId: "conocemibarrio",' \
#          '        storageBucket: "conocemibarrio.appspot.com",' \
#          '        messagingSenderId: "497938302411",' \
#          '        appId: "1:497938302411:web:cd5cea068c5df16ca1e24e",' \
#          ' };' \
#          'firebase.initializeApp(firebaseConfig);' \
#          'const messaging=firebase.messaging();' \
#          'messaging.setBackgroundMessageHandler(function (payload) {' \
#          '    console.log(payload);' \
#          '    const notification=JSON.parse(payload);' \
#          '    const notificationOption={' \
#          '        body:notification.body,' \
#          '        icon:notification.icon' \
#          '    };' \
#          '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
#          '});'
#
#     return HttpResponse(data, content_type="text/javascript")
#
#
# def sendNotification(registration_ids, message_title, message_desc):
#     fcm_api = "AAAAc-9vhcs:APA91bF32L5PxwnY3QG1VJ1wsPjeWW6h5ozkTwjzNO9CeQ_J-nMUgkDQMeszaJVBAeOgTXwgNe0XWwjyHLyNA6jUtf3X59zJvK4aknJhkXaJ5Ze_L6ZrZ3PYgEWy549oA0diUHFo0ITy"
#     url = "https://fcm.googleapis.com/fcm/send"
#
#     headers = {
#         "Content-Type": "application/json",
#          "Authorization": 'key='+fcm_api}
#
#     payload = {
#         "registration_ids": registration_ids,
#         "priority": "high",
#         "notification": {
#             "body": message_desc,
#             "title": message_title,
#             "image": "/static/img/logo.png",
#             "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
#
#         }
#     }
#
#     result = requests.post(url,  data=json.dumps(payload), headers=headers)
#     print(result.json())
#
#
# def send(request):
#     registration = ['cYe5DrcQGn6hdZSn1QSTbn:APA91bEiyIjngtGsivld2RE2w7vFytPB5tnf32nU8VHV545nGJF7OoQOce-MeovEqxCqZrT84NUaEjwjx0xI0ezNonkmO7dlaMVFPCTn7iwiFSiIw-cVHyTQAymIIyaR99Ru67COIiFN']
#     sendNotification(registration, 'Code Keen added a new video', 'Code Keen new video alert')
#     return HttpResponse("sent")
#
#
# @require_POST
# @csrf_exempt
# def send_push(request):
#     try:
#         logger.info(request.body)
#         body = request.body
#         data = json.loads(body)
#
#         if 'head' not in data or 'body' not in data or 'id' not in data:
#             logger.info("invalid data format")
#             return JsonResponse(status=400, data={"message": "Invalid data format"})
#
#         user_id = data['id']
#         user = get_object_or_404(User, pk=user_id)
#         payload = {'head': data['head'], 'body': data['body']}
#         # send_user_notification(user=user, payload=payload, ttl=1000)
#         logger.info("web pushh successful")
#         return JsonResponse(status=200, data={"message": "Web push successful"})
#     except TypeError:
#         logger.info("an error occurred")
#         return JsonResponse(status=500, data={"message": "An error occurred"})
