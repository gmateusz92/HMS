from hotelbooking.models import Room
from hotelbooking.forms import AvalilabilityForm
from django.shortcuts import render

def get_room_category_human_format(category):
    room = Room.objects.all[0]
    room_category = dict(room.ROOM_CATEGORIES).get(category, None)
    return room_category

