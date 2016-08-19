from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^my/$', views.events_my, name='my'),
    url(r'^attended/$', views.events_attended, name='attended'),
    url(r'^invited/$', views.events_invited, name='invited'),
    url(r'^event/(?P<pk>[0-9]+)/$', views.event_page, name='event_page'),
]
