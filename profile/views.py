from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UpdateUserForm, UpdateProfileForm
from .models import Profile


@login_required
def profile(request):
    # create instances of those forms depending on whether the request is get or post.
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if 'image-file' in request.FILES:
            avatar = request.FILES['image-file']
            user_profile = Profile.objects.get(user_id=request.user.id)
            print("TODALOO")
            print(user_profile.id)
            user_profile.avatar = avatar
            user_profile.save()

        # ver cómo se pasa data FILES en cloudinary
        # profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid(): # and profile_form.is_valid():
            user_form.save()
            # profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('/profile/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    # return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})
    return render(request, 'profile.html', {'user_form': user_form})
