from django.urls import path
from app import views

urlpatterns = [
    path('home/',views.HomeView.as_view(),name='home'),

]