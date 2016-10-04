from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.MainPage.as_view(), name='index'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^my/$', views.MyEvents.as_view(), name='my'),
    url(r'^attended/$', views.AttendedEvents.as_view(), name='attended'),
    url(r'^invited/$', views.InvitedEvents.as_view(), name='invited'),
    url(r'^event/(?P<pk>[0-9]+)/$', views.EventPage.as_view(),
        name='event_page'),
    ]
