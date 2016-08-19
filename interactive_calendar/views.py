from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Event
from .forms import EventForm, UserForm
import datetime


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
    else:
        user_form = UserForm()
        return render(request, 'interactive_calendar/register.html',
                      {'user_form': user_form,
                       'registered': registered}
                      )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Sorry, disabled account')
        else:
            return HttpResponse('Sorry, invalid login')

    else:
        return render(request, 'interactive_calendar/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def index(request):
    if 'post_event' in request.POST:
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.attenders = None
            event.invited = None
            event.save()
            return redirect('index')
    else:
        form = EventForm()

    if 'datepicker' in request.POST:
        event_date = request.POST.get('datepicker')
        event_date = datetime.datetime.strptime(event_date, '%m/%d/%Y').date()
        ev = Event.objects.filter(date_start__year=event_date.year,
                                  date_start__month=event_date.month,
                                  date_start__day=event_date.day,
                                  private=False)
        return render(request, 'interactive_calendar/index.html',
                      {'form': form, 'ev': ev})

    return render(request, 'interactive_calendar/index.html', {'form': form})


@login_required
def events_my(request):
    event = Event.objects.filter(author=request.user).order_by('date_start')
    return render(
        request, 'interactive_calendar/event_list.html',
        {'event': event})


@login_required
def events_attended(request):
    author = str(request.user)
    event = Event.objects.filter(attenders__contains=[author])
    return render(
        request, 'interactive_calendar/event_list.html',
        {'event': event})


@login_required
def events_invited(request):
    author = str(request.user)
    event = Event.objects.filter(invited__contains=[author])
    return render(
        request, 'interactive_calendar/event_list.html',
        {'event': event})


@login_required
def event_page(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if 'invite' in request.POST:
        username = request.POST.get('username')
        if User.objects.filter(username=str(username)).exists():
            event.invited.append(str(username))
            event.save()

    if 'attend' in request.POST:
        if event.attenders is None:
            event.attenders = [str(request.user)]
        else:
            event.attenders.append(str(request.user))
        event.save()

    if 'not_attend' in request.POST:
        event.attenders.remove(str(request.user))
        event.save()

    if event.attenders is None:
        pass
    else:
        event.attenders_num = len(event.attenders)

    if event.invited is not None:
        event.invited = list(set(event.invited))
    if event.attenders is not None:
        event.attenders = list(set(event.attenders))

    if event.invited and event.attenders is not None:
        for i in event.invited:
            if i in event.attenders:
                event.invited.remove(i)

    event.save()

    return render(
        request, 'interactive_calendar/event_page.html',
        {'event': event, }, )
