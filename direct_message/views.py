from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from direct_message.models import Message

@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_dm = None
    directs = None

    if messages:
        message = messages[0]
        active_dm = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_dm:
                message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_dm': active_dm,
    }
    
    template = loader.get_template('dm/direct.html')

    return HttpResponse(template.render(context, request))
