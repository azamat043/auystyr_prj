from django.shortcuts import render

from core.models import Event


def events(request):
    events = Event.objects.all()

    context = {
        "events": events
    }

    return render(request, 'events/events.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)

    context = {
        "event": event
    }

    return render(request, 'events/event_detail.html', context)
