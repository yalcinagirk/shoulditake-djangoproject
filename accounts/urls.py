from django.urls import include, path
from accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(),name='login'),
    path('register/', views.RegisterView.as_view(),name='register'),
    path('logout/', views.LogoutView.as_view(),name='logout'),
]
