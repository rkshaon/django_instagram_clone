from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification

def show_notification(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_seen=False).order_by('-date')

    template = loader.get_template('notifications.html')

    context = {
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))

def delete_notification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()

    return redirect('show_notification')

def count_notification(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

    return {'count_notifications': count_notifications}
