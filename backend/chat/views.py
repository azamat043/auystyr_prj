import json

from django.db.models import Q, Max
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Message
from userauths.models import User


def chat(request):
    contacts = User.objects.exclude(id=request.user.id).annotate(
        last_message_date=Max('received_messages__date')
    ).order_by('-last_message_date')

    contact_info = []
    for contact in contacts:
        contact_info.append({
            'user_id': contact.id,
            'name': contact.full_name if contact.full_name else contact.username,
            'image': contact.profile.image.url if contact.profile.image else '',
            'message': contact.received_messages.filter(Q(sender=request.user) | Q(receiver=request.user)).last().text if contact.received_messages.filter(Q(sender=request.user) | Q(receiver=request.user)).last() else '',
            "last_message_date": contact.last_message_date.strftime('%H:%M') if contact.last_message_date else '',
        })

    context = {
        'contacts': contact_info
    }

    return render(request, 'chat/chat.html', context)


def get_message_with_user(request, user_id):
    user = User.objects.get(id=user_id)

    messages = Message.objects.filter(sender=request.user, receiver=user) | Message.objects.filter(sender=user, receiver=request.user)
    messages = messages.order_by('date')

    data = []

    chat_user = {
        "chat_user_id": user.id,
        "request_user_id": request.user.id,
        "chat_user_name": user.full_name if user.full_name else user.username,
        "chat_user_image": user.profile.image.url if user.profile.image else '',
    }

    for message in messages:
        data.append({
            'sender_name': message.sender.full_name if message.sender.full_name else message.sender.username,
            'sender_image': message.sender.profile.image.url if message.sender.profile.image else '',
            'receiver_name': message.receiver.full_name if message.receiver.full_name else message.receiver.username,
            'receiver_image': message.receiver.profile.image.url if message.receiver.profile.image else '',
            'text': message.text,
            'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
            'sender': 'me' if message.sender == request.user else ''
        })

    return JsonResponse({'messages': data, "chat_user": chat_user})


@csrf_exempt
def send_message_to_user(request, user_id):
    user = User.objects.get(id=user_id)
    data = json.loads(request.body)
    text = data.get('message')

    message = Message(sender=request.user, receiver=user, text=text)
    message.save()

    return JsonResponse({'status': 200})
