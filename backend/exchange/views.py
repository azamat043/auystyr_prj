from django.shortcuts import render
from core.models import BookExchangeRequest


def exchange(request):
    exchange_request = BookExchangeRequest.objects.all()

    incoming = exchange_request.filter(receiver=request.user)
    outgoing = exchange_request.filter(sender=request.user)

    context = {
        'incoming': incoming,
        'outgoing': outgoing
    }

    return render(request, 'exchange/exchange.html', context)
