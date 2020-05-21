from django.urls import path
from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^home', views.HomeView.as_view(), name='home'),
    url(r'^profile', views.ProfileView.as_view(), name='profile'),
    url(r'^contact', views.ContactView.as_view(), name='contact'),
    url(r'^reviews', views.ReviewsView.as_view(), name='reviews'),
    url(r'^articles/$', views.ArticleList, name='articles'),
    url(r'^article_create/$', views.ArticleCreate, name='articlecreate'),
    url(r'^article_update/(?P<slug>[-\w]+)/$', views.ArticleUpdate, name='articleupdate'),
    url(r'^details/(?P<slug>[-\w]+)/$', views.ArticleDetails, name='details'),
    url(r'^add-comment/(?P<slug>[-\w]+)/$', views.add_comment, name='add-comment'),
    url(r'^add-remove-favorite/(?P<slug>[-\w]+)/$', views.add_or_remove_favorite, name='add-remove-favorite'),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.ArticleDelete, name='articledelete'),

]
