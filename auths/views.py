from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from app.models import Product
from auths.decorators import anonymous_required
from auths.forms import RegisterForm, LoginForm, UserProfileUpdateForm, UserPasswordChangeForm, UserPasswordChangeForm2
# Create your views here.
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from auths.models import UserProfile
from django.contrib.auth.decorators import login_required

from following.models import Following


@anonymous_required
def register(request):
    """ alternative of anonymous decorator
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('articles'))
    """
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(user.userprofile.get_user_profile_url())
    return render(request, 'auth/register.html', context={'form': form})


@anonymous_required
def user_login(request):
    """ alternative of anonymous decorator
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('articles'))
    """
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                msg = "<b>Merhaba %s. Sisteme Hoşgeldiniz.</b>" % (username)
                return HttpResponseRedirect(reverse('articles'))
    return render(request, 'auth/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('articles'))


@login_required
def user_profile(request, username):
    takip_ediyor_mu = False
    user = get_object_or_404(User, username=username)
    article_list = Product.objects.filter(user=user)
    takipci_ve_takip_edilen = Following.kullaniciyi_takip_edilenler_ve_takipciler(user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']
    if user != request.user:
        takip_ediyor_mu = Following.kullaniciyi_takip_ediyor_mu(follower=request.user, followed=user)


    return render(request, 'auth/profile/user_profile.html',
                  context={'user': user,
                           'takipciler': takipciler,
                           'takip_edilenler': takip_edilenler,
                           'takip_ediyor_mu': takip_ediyor_mu,
                           'article_list': article_list,
                           'page': 'user_profile'

                           }
                  )


def user_settings(request):
    cinsiyet = request.user.userprofile.cinsiyet
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    # dogum_tarihi = request.user.userprofile.dogum_tarihi
    initial = {'cinsiyet': cinsiyet, 'bio': bio, 'profile_photo': profile_photo}
    form = UserProfileUpdateForm(initial=initial, instance=request.user, data=request.POST or None,
                                 files=request.FILES or None)
    takipci_ve_takip_edilen = Following.kullaniciyi_takip_edilenler_ve_takipciler(request.user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']
    if form.is_valid():
        user = form.save(commit=True)
        bio = form.cleaned_data.get('bio', None)
        cinsiyet = form.cleaned_data.get('cinsiyet', None)
        profile_photo = form.cleaned_data.get('profile_photo', None)
        email = form.cleaned_data.get('email', None)
        print("email",email)
        user.userprofile.cinsiyet = cinsiyet
        user.userprofile.bio = bio
        user.userprofile.email = email
        user.userprofile.profile_photo = profile_photo
        user.userprofile.save()
        return HttpResponseRedirect(reverse('user_profile', kwargs={'username': user.username}))

    return render(request, 'auth/profile/settings.html',
                  context={'form': form,
                           'takipciler': takipciler,
                           'takip_edilenler': takip_edilenler,
                           })


def user_about(request, username):
    user = get_object_or_404(User, username=username)
    takip_ediyor_mu = False
    takipci_ve_takip_edilen = Following.kullaniciyi_takip_edilenler_ve_takipciler(user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    if user != request.user:
        takip_ediyor_mu = Following.kullaniciyi_takip_ediyor_mu(follower=request.user, followed=user)

    return render(request, 'auth/profile/about_me.html',
                  context={'user': user,
                           'page': 'about',
                           'takipciler': takipciler,
                           'takip_edilenler': takip_edilenler,
                           'takip_ediyor_mu': takip_ediyor_mu,
                           })


def user_password_change(request):
    # form = UserPasswordChangeForm(user=request.user, data=request.POST or None)
    form = UserPasswordChangeForm2(user=request.user, data=request.POST or None)
    takipci_ve_takip_edilen = Following.kullaniciyi_takip_edilenler_ve_takipciler(request.user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    if form.is_valid():
        user = form.save(commit=True)
        update_session_auth_hash(request, user)
        # new_password = form.cleaned_data.get('new_password')
        # request.user.set_password(new_password)
        # request.user.save()
        # update_session_auth_hash(request, request.user)
        return HttpResponseRedirect(reverse('user_profile', kwargs={'username': request.user.username}))
    return render(request, 'auth/profile/password_change.html',
                  context={'form': form,
                           'page': 'change',
                           'takipciler': takipciler,
                           'takip_edilenler': takip_edilenler,
                           })
