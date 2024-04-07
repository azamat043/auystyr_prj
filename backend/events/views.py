from datetime import datetime

from django.shortcuts import render, redirect

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


def event_create(request):
    if request.method == 'POST' and request.FILES:
        title = request.POST.get('title')
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')
        date_day = request.POST.get('event-date')
        date_time = request.POST.get('event-time')
        image = request.FILES.get('image')

        date = datetime.strptime(date_day + ' ' + date_time, '%Y-%m-%d %H:%M')

        print(request.POST, request.FILES)

        try:
            event = Event.objects.create(
                user=request.user,
                title=title,
                description=description,
                visibility=visibility,
                date=date,
                image=image
            )
            event.save()
            if event:
                return redirect('events')

            return render(request, 'events/event_create.html', {"error": "Failed to create event. Please try again."})
        except Exception as e:
            return render(request, 'events/event_create.html', {"error": str(e)})

    return render(request, 'events/event_create.html')
