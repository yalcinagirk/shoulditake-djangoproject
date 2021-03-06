from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.generic import FormView

from accounts.forms import UserCreateForm


class LoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreateForm
    success_url = 'app/home/home.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # for autologin
        # user = authenticate(username=username, password=password)
        # login(self.request, user)
        return redirect('home')

    def register(request):

        if request.method == 'POST':
            form = UserCreationForm(request.POST or None)
            if form.is_valid():
                form.save()
                return redirect('home')


            else:
                return render(request, '../templates/app/home', {'form': form})
        else:
            form = UserCreationForm()
            return render(request, '../templates/app/home', {'form': form})


class LogoutView(LogoutView):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
