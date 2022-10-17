from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, FormView
from .models import Room, Booking
from .forms import AvalilabilityForm
from hotelbooking.booking_funkctions.availibility import check_availability
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def room_detail_view(request, room_pk):
    room_detail = get_object_or_404(Room, pk=room_pk) #mozna dawać room_pk albo room_id
    context = {'room_detail': room_detail}
    return render(request, 'room_detail.html', context)

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
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('this category of rooms are booked')