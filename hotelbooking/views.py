from django.shortcuts import render
from django.views.generic import ListView, FormView
from .models import Room, Booking
from .forms import AvalilabilityForm
from hotelbooking.booking_funkctions.availibility import check_availability
from django.http import HttpResponse

class RoomList(ListView):
    model = Room
    template_name = 'room_list.html'

class BookingList(ListView):
    model = Booking
    template_name = 'booking_list.html'

class BookingView(FormView):
    form_class = AvalilabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data # pobieramy data z wypelnionego formularza
        room_list = Room.objects.filter(category=data['room_category'])
        available_rooms=[]
        for room in room_list: #jezeli True to dodajemy do avaialbe_rooms[]
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms)>0: #jezeli jest cos na liscie czyli lista jest > 0
            room = available_rooms[0]# dla pierwszego z listy wolnego pokoju towrzymy rezerwacje
            booking = Booking.objects.create(
                user = request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('this category of rooms are booked')