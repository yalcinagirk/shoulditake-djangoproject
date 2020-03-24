from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class UserCreateForm(forms.Form):
    username = forms.CharField(label='Username', min_length=4, max_length=30)
    name = forms.CharField(label='name', min_length=4, max_length=30)
    surname = forms.CharField(label='surname', min_length=4, max_length=30)
    #department = forms.CharField(max_length=100)
    file = forms.FileField()
    #image = forms.ImageField(help_text="Upload image: ", required=False)
    #job =forms.CharField(label='job', min_length=2, max_length=30)
    email = forms.EmailField(label='E-mail', )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['name'],
            last_name=self.cleaned_data['surname'],
            #department=self.cleaned_data['department'],
            file=self.cleaned_data['file'],)