from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import MessageForm
from .models import Message, NeighborhoodChat
from registration.models import Neighborhood, UserNeighborhood

@login_required
def chat(request):
    user = request.user
    user_neighborhood = UserNeighborhood.objects.get(user_id=user.pk)
    neighborhood = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    neighborhood_chat = NeighborhoodChat.objects.get(neighborhood=neighborhood)
    if (neighborhood_chat == None):
        neighborhood_chat = NeighborhoodChat(neighborhood=neighborhood)
        neighborhood_chat.save()
    messages = Message.objects.filter(chat=neighborhood_chat)
    if(request.method == 'POST'):
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
            'neighbothood': neighborhood,
        },
    )
