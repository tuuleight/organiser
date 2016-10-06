import datetime
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Event
from .forms import EventForm, UserForm


class RegisterView(View):
    template_name = 'interactive_calendar/register.html'
    user_form = UserForm
    registered = False

    def get(self, request, *args, **kwargs):
        form = self.user_form()
        registered = self.registered

        return render(request, self.template_name, {'form': form,
                                                    'registered': registered})

    def post(self, request, *args, **kwargs):
        form = self.user_form(request.POST)

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            return HttpResponse('User already created')

        return render(request, self.template_name, {'form': form,
                                                    'registered': registered})


class LoginView(View):
    template_name = 'interactive_calendar/login.html'
    user_form = UserForm

    def get(self, request, *args, **kwargs):
        form = self.user_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Sorry, disabled account')
        else:
            return HttpResponse('Sorry, invalid login')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class MainPage(View):
    """
    Main page with form to create new events and calendar to search for events
    """
    form_class = EventForm
    template_name = 'interactive_calendar/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """handle post request from calendar search and filled form"""
        form = self.form_class()

        if 'datepicker' in request.POST:
            event_date = request.POST.get('datepicker')
            event_date = datetime.datetime.strptime(event_date,
                                                    '%m/%d/%Y').date()
            ev = Event.objects.filter(date_start__year=event_date.year,
                                      date_start__month=event_date.month,
                                      date_start__day=event_date.day,
                                      private=False)
            return render(request, self.template_name, {'form': form, 'ev': ev})

        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.author = request.user
                event.attenders = None
                event.invited = None
                event.save()
                return redirect('index')
            return render(request, self.template_name, {'form': form})


class EventsList(ListView):
    """
    Class providing template and context to inheriting events list class
    """
    template_name = 'interactive_calendar/event_list.html'
    context_object_name = 'event'


class MyEvents(EventsList):
    """
    For events created by current user
    """
    def get_queryset(self):
        return Event.objects.filter(author=self.request.user).order_by(
            'date_start')


class AttendedEvents(EventsList):
    """
    For events in which current user participates
    """
    def get_queryset(self):
        author = str(self.request.user)
        return Event.objects.filter(attenders__contains=[author])


class InvitedEvents(EventsList):
    """
    For events where current user is listed as 'invited'
    """
    def get_queryset(self):
        author = str(self.request.user)
        return Event.objects.filter(invited__contains=[author])


class EventPage(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'interactive_calendar/event_page.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'invite' in request.POST:
            username = request.POST.get('username')
            us = User.objects.filter(username=str(username)).exists()
            if us:
                self.object.update_invited(str(username))
                self.object.save()

        if 'attend' in request.POST:
            name = str(request.user)
            self.object.add_attenders(name)
            self.object.save()

        if 'not_attend' in request.POST:
            name = str(request.user)
            self.object.del_attenders(name)
            self.object.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
