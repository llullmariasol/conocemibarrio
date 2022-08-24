from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import MessageForm
from .models import Message, NeighborhoodChat
from registration.models import Neighborhood, UserNeighborhood

@login_required
def chat(request):
    user = request.user
    try:
        user_neighborhood = UserNeighborhood.objects.get(user_id=user.pk)
    except UserNeighborhood.DoesNotExist:
        return render(
            request,
            'join_a_neighborhood.html',
            {'function': "chat barrial"}
        )
    neighborhood = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    neighborhood_chat, created = NeighborhoodChat.objects.get_or_create(neighborhood=neighborhood)
    if created:
        neighborhood_chat.save()
    messages = Message.objects.filter(chat=neighborhood_chat)
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = neighborhood_chat
            message.user = user
            message.save()
    else:
        form = MessageForm()
    return render(
        request,
        'chat.html',
        {
            'form': form,
            'msgs': messages,
            'neighborhood': neighborhood,
        },
    )
