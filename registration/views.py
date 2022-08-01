import threading

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.conf import settings
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json

from .forms import (RegistrationForm,
                    LogInForm,
                    JoinNeighborhoodForm)
from .models import Neighborhood, UserNeighborhood

UserModel = get_user_model()


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def home(request):
    args = {}
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    if request.user.is_authenticated:
        users_neighborhoods = UserNeighborhood.objects.all()
        if users_neighborhoods is not None:
            for user_neighborhood in users_neighborhoods:
                if user_neighborhood.user == request.user:
                    args['neighborhood'] = user_neighborhood
                    neighborhood_id = user_neighborhood.neighborhood.pk
                    break

        if request.user.groups.all().exists() and request.user.groups.all()[0].name == "neighborhood-admin":
            n = Neighborhood.objects.get(pk=neighborhood_id)
            args['n'] = n

    neighborhoods = Neighborhood.objects.filter(is_active=1)
    args['neighborhoods'] = list(neighborhoods)
    args['vapid_key'] = vapid_key

    return render(request, 'base.html', args)


def registration(request):
    args = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        neighborhoods = Neighborhood.objects.filter(is_active=1)
        args['neighborhoods'] = neighborhoods

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            if request.POST.get('barrio'):
                neighborhood_id = request.POST.get('barrio')
                n = Neighborhood.objects.get(pk=neighborhood_id)
                user_neighborhood = UserNeighborhood()
                user_neighborhood.user = user
                user_neighborhood.neighborhood = n
                user_neighborhood.justification = None
                user_neighborhood.save()

            current_site = get_current_site(request)
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_subject = 'Activá tu cuenta'
            to_email = form.cleaned_data.get('email')
            email_message = mail.EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email]
            )

            EmailThread(email_message).start()
            messages.add_message(request, messages.SUCCESS, "El link para activar tu cuenta fue enviado.")

            return HttpResponseRedirect('/')
    else:
        neighborhoods = Neighborhood.objects.filter(is_active=1)
        form = RegistrationForm()
        args['neighborhoods'] = neighborhoods
    args['form'] = form

    return render(request, 'registration.html', args)


def registrationNeighborhoodAdmin(request):
    args = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        neighborhoods = Neighborhood.objects.all()
        args['neighborhoods'] = neighborhoods

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            group = Group.objects.get(name='neighborhood-admin')
            user.save()
            user.groups.add(group)
            user.save()

            if request.POST.get('barrio'):
                neighborhood_id = request.POST.get('barrio')
                n = Neighborhood.objects.get(pk=neighborhood_id)
                user_neighborhood = UserNeighborhood()
                user_neighborhood.user = user
                user_neighborhood.neighborhood = n
                user_neighborhood.justification = request.POST.get('justification')
                user_neighborhood.save()

            message = render_to_string('registration_neighborhood_admin_mail.html', {
                'user': user,
                'neighborhood': n.name,
            })
            email_subject = 'Solicitud de registro'
            to_email = form.cleaned_data.get('email')
            email_message = mail.EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email]
            )

            EmailThread(email_message).start()
            messages.add_message(request, messages.SUCCESS, "Procesaremos tu solicitud y te avisaremos vía mail.")

            return HttpResponseRedirect('/')
    else:
        neighborhoods = Neighborhood.objects.all()
        form = RegistrationForm()
        args['neighborhoods'] = neighborhoods
    args['form'] = form

    return render(request, 'registration_neighborhood_admin.html', args)


def activation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.signup_confirmation = True
        user.save()
        messages.success(request, 'Usuario registrado con éxito. Inicie sesion.')
        return HttpResponseRedirect('/login')
    else:
        messages.warning(request, 'Link de activacion inválido.')
        return HttpResponseRedirect('/')
    return render(request, 'base.html', {})


def logIn(request):
    args = {}
    valueNext = request.POST.get('next')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if valueNext:
                        return HttpResponseRedirect(valueNext)
                    else:
                        return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/home')
    else:
        form = LogInForm()

    args['form'] = form

    return render(request, 'login.html', args)


def logOut(request):
    logout(request)
    return HttpResponseRedirect('/')

    return render(request, 'base.html', {})


def joinNeighborhood(request):
    args = {}
    user = request.user
    if request.method == 'POST':
        form = JoinNeighborhoodForm(request.POST)

        if form.is_valid():
            if request.POST.get('barrio'):
                neighborhood_id = request.POST.get('barrio')
                n = Neighborhood.objects.get(pk=neighborhood_id)
                user_neighborhood = UserNeighborhood()
                user_neighborhood.user = user
                user_neighborhood.neighborhood = n
                user_neighborhood.save()

            return HttpResponseRedirect('/')
    else:
        neighborhoods = Neighborhood.objects.filter(is_active=1)
        form = JoinNeighborhoodForm()
        args['neighborhoods'] = neighborhoods
    args['form'] = form

    return render(request, 'join_neighborhood.html', args)


@login_required
def administrationRequests(request):
    args = {}
    group = Group.objects.all().filter(name='neighborhood-admin').first()
    users = group.user_set.all().filter(is_active=0)  # users que quieren ser administradores de barrios
    current_neighborhood_admins = list(group.user_set.all().filter(is_active=1))
    users_neighborhoods = UserNeighborhood.objects.all().filter(rejected=0)
    users_list = []
    if len(users) > 0:
        for u in users_neighborhoods:
            try:
                users.get(id=u.user.id)
                users_list.append(u)
            except User.DoesNotExist:
                pass

    # lista de barrios que ya tienen administradores
    neighborhoods_with_admin = []
    #recorrer user_neighborhood tabla, si el user id está en current_neighborhood_admins,
    #agregar el neighborhood id a neighborhoods_with_admin
    users_neighborhoods_list = list(UserNeighborhood.objects.all())
    for un in users_neighborhoods_list:
        for c in current_neighborhood_admins:
            if un.user.id == c.id:
                neighborhoods_with_admin.append(un.neighborhood.id)

    new_list = []
    # si el user de la request es administrador general
    # recorrer la lista de usuarios y eliminar cuyo barrio ya tiene admin
    if request.user.is_superuser:
        for x in users_list:
            if x.neighborhood.id not in neighborhoods_with_admin:
                new_list.append(x)
        args['users_list'] = new_list
    else:
        # si el user de la request es administrador de un barrio
        #buscar solicitudes de ese barrio
        if request.user.groups.all().exists() and request.user.groups.all()[0].name == "neighborhood-admin":
            admin = UserNeighborhood.objects.all().filter(user=request.user).first()
            for y in users_list:
                if y.neighborhood.id == admin.neighborhood.id:
                    new_list.append(y)

    args['users_list'] = new_list
    return render(request, 'administration_requests.html', args)


@login_required
def approveAdministrationRequest(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = True
    user.signup_confirmation = True
    user.save()

    user_neighborhood = UserNeighborhood.objects.all().filter(user=user).first()
    n = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    current_site = get_current_site(request)
    message = render_to_string('neighborhood_admin_request_approved.html', {
        'user': user,
        'domain': current_site.domain,
        'neighborhood': n.name,
    })
    email_subject = 'Aprobamos tu solicitud'
    to_email = str(user.email)

    email_message = mail.EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email]
    )

    EmailThread(email_message).start()

    args = {}
    group = Group.objects.all().filter(name='neighborhood-admin').first()
    users = group.user_set.all().filter(is_active=0)
    users_neighborhoods = UserNeighborhood.objects.all().filter(rejected=0)
    users_list = []
    if len(users) > 0:
        for u in users_neighborhoods:
            try:
                users.get(id=u.user.id)
                users_list.append(u)
            except User.DoesNotExist:
                pass

    args['users_list'] = users_list

    return render(request, 'administration_requests.html', args)


@login_required
def rejectAdministrationRequest(request, pk):
    user = User.objects.get(pk=pk)
    user_neighborhood = UserNeighborhood.objects.all().filter(user=user).first()
    user_neighborhood.rejected = True
    user_neighborhood.save()
    n = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    current_site = get_current_site(request)
    message = render_to_string('neighborhood_admin_request_rejected.html', {
        'user': user,
        'domain': current_site.domain,
        'neighborhood': n.name,
    })

    email_subject = 'Rechazamos tu solicitud'
    to_email = str(user.email)
    email_message = mail.EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email]
    )

    EmailThread(email_message).start()

    args = {}
    group = Group.objects.all().filter(name='neighborhood-admin').first()
    users = group.user_set.all().filter(is_active=0)
    users_neighborhoods = UserNeighborhood.objects.all().filter(rejected=0)
    users_list = []
    if len(users) > 0 and len(users_neighborhoods) > 0:
        for u in users_neighborhoods:
            try:
                users.get(id=u.user.id)
                users_list.append(u)
            except User.DoesNotExist:
                pass

    args['users_list'] = users_list

    return render(request, 'administration_requests.html', args)


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)
        print("PUSH")
        print(user_id)
        print(payload)
        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
