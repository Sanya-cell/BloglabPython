from django.contrib import admin
from django.urls import path, re_path

from blogelements import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    re_path(r'^article/(?P<article_id>[0-9]+)/$', views.show_article, name='article'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('me/', views.me, name='me'),
    path('logout/', views.doLogout, name='logout'),

]
