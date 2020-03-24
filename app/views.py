from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class HomeView( TemplateView):
    template_name = "home/home.html"
class ProfileView( TemplateView):
    template_name = "profile/public_profile.html"
class ContactView( TemplateView):
    template_name = "profile/profile_contact.html"
class ReviewsView( TemplateView):
    template_name = "profile/profile_reviews.html"