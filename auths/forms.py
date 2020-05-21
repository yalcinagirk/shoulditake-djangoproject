from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re
from auths.models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(min_length=5, label='Password Confirm', required=True,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password', 'Parolalar Eşleşmedi')
            self.add_error('password_confirm', 'Parolalar Eşleşmedi')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email sistemde kayıtlı.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = username.lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu Kullanıcı Adı sistemde kayıtlı.')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-class'}))
    password = forms.CharField(required=True, max_length=50, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-class'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            self.add_error('password', 'Parolala veya şifre yanlış')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            users = User.objects.filter(email__iexact=username)
            if len(users) > 0 and len(users) == 1:
                return users.first().username
        return username


class UserProfileUpdateForm(forms.ModelForm):
    cinsiyet = forms.ChoiceField(required=True, choices=UserProfile.Cinsiyet)
    profile_photo = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    # dogum_tarihi = forms.DateField(input_formats=("%d.%m.%Y",), widget=forms.DateInput(format="%d.%m.%Y"),
    #                              required=True, label='Doğum Tarihi')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'cinsiyet', 'profile_photo', 'bio']

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['bio'].widget.attrs['rows'] = 10

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if not email:
            raise forms.ValidationError('Bu e-mail sistemde mevcut.')



class UserPasswordChangeForm(forms.Form):
    user = None
    old_password = forms.CharField(min_length=8, required=True, label="Mevcut şifreniz.",
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(min_length=8, required=True, label="Yeni şifreniz.",
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password_confirm = forms.CharField(min_length=8, required=True, label="Şifrenizi doğrulayın.",
                                           widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')

        if new_password != new_password_confirm:
            self.add_error('new_password', 'Şifreler eşleşmedi')
            self.add_error('new_password_confirm', 'Şifreler eşleşmedi')

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Eski şifre eşleşmedi.')
        return old_password


class UserPasswordChangeForm2(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserPasswordChangeForm2, self).__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
