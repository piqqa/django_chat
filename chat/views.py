# chat/views.py
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

@login_required
def index(request):
    users = User.objects.all().filter(~Q(id = request.user.id))
    return render(request, 'chat/index.html', {
        'user_list': users
    })

@login_required
def room(request, is_private, room_name):
    actual_room_name = room_name
    #in case of private room_name is username of another user
    private = True if is_private == "private" else False
    if private:
        request_username = request.user.username
        actual_room_name = actual_room_name + "|"+ request_username if actual_room_name < request_username \
            else request_username + "|" + actual_room_name
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(actual_room_name)),
        'is_private': json.dumps(private)
    })
