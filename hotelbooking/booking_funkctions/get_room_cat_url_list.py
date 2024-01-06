from hotelbooking.models import Room
from django.urls import reverse


#funkcja zwracajaca room category i url liste

def get_room_cat_url_list():
    room = Room.objects.all()[0] #pobiera pierwszy losowy room object
    room_categories = dict(room.ROOM_CATEGORIES)  # tworzy slownik z tuple
    room_cat_url_list = [] # pusta lista category, URL


    for category in room_categories:
        room_category = room_categories.get(category) #room_category=value, category=key
        room_url = reverse('hotelbooking:room_detail', kwargs={'category': category})
        room_cat_url_list.append((room_category, room_url))
    return room_cat_url_list

#gotowa lista par (nazwa kategorii, URL): [('AC', '/room/detail/AC/'),