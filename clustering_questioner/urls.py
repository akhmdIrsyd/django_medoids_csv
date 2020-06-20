from django.conf.urls import url, include
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from .views import data_list

from . import views

urlpatterns = [
    url(r'^visual/$', views.visual, name='visual'),
    url(r'^cluster/$', views.cluster_list, name='cluster'),
    url(r'^$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^data/$', data_list, name='data'),
    url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    url(r'^update/(?P<id>\d+)/', views.update, name='update'),
    url(r'^home2/$', views.index2, name='index2'),
    
]
