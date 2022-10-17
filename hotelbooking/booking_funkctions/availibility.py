from datetime import datetime, date
import datetime
from hotelbooking.models import Room, Booking

def check_availability(room, check_in, check_out): #sprawdza dosttepnosć pokoju
    avail_list = [] #ta lista tworzy true or false
    booking_list = Booking.objects.filter(room=room)
    for booking in booking_list:
        if booking.check_in.date() > check_out or booking.check_out.date() < check_in: #booking.check_in to istniejaca juz rezerwacja (tak samo booking.check_out
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list) #all zwraca True jezeli wszystkie argumenty w liscie to True