from django.urls import path
from app import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('reviews/',views.ReviewsView.as_view(),name='reviews'),

]