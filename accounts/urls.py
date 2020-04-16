from django.urls import include, path
from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view(),name='login'),
    url(r'^register/', views.RegisterView.as_view(),name='register'),
    url(r'^logout/', views.LogoutView.as_view(),name='logout'),
]
