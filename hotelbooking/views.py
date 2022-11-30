from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, FormView, View, DeleteView, DetailView
from .models import Room, Booking
from .forms import AvalilabilityForm
from hotelbooking.booking_funkctions.availibility import check_availability
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django_event_cal.functions import cal_context
from datetime import datetime, date
from django.utils.safestring import mark_safe
from .models import *
from .utils import Calendar

def home(request):
     # context = {}
     # context = cal_context(context, year, month, True)
     # return render(request, 'home.html', context)
     return render(request, 'home.html')

def room_detail_view(request, room_pk):
    room_detail = get_object_or_404(Room, pk=room_pk) #mozna dawać room_pk albo room_id
    context = {'room_detail': room_detail}
    return render(request, 'room_detail.html', context)


def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    room_values = room_categories.values()
    room_list = []

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('hotelbooking:RoomDetailView', kwargs={'category': room_category})
        room_list.append((room, room_url))
    context = {
        'room_list': room_list,
        'room': room,
    }
    return render(request, 'room_list.html', context)


# class RoomListView(ListView):
#     model = Room
#     template_name = 'room_list.html'

class BookingList(ListView): #wyswietla rezerwacje uzytkowników
    model = Booking
    template_name = 'booking_list.html'
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class RoomDetailView(View): #tworzymy do zrezerwacji z formularzy POST Get
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None) #dlaczego kwargs
        form = AvalilabilityForm()
        room_list = Room.objects.filter(category=category) #dlaczego room_category

        if len(room_list) > 0:
            room = room_list[0]  # pierwszy z listy
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None) #pobieramy kategorie z modelu i z niej pobieramy kategorie
            context = {
                'room_category': room.category,
                'form': AvalilabilityForm,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)  # dlaczego kwargs
        room_list = Room.objects.filter(category=category)
        form = AvalilabilityForm(request.POST) #pobiera z post

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:  # jezeli True to dodajemy do avaialbe_rooms[]
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:  # jezeli jest cos na liscie czyli lista jest > 0
            room = available_rooms[0]  # dla pierwszego z listy wolnego pokoju towrzymy rezerwacje
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('this category of rooms are booked')



class RoomDetailView(View): #tworzymy do zrezerwacji z formularzy POST Get
    model = Room
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None) #dlaczego kwargs
        form = AvalilabilityForm()
        room_list = Room.objects.filter(category=category) #dlaczego room_category

        if len(room_list) > 0:
            room = room_list[0]  # pierwszy z listy
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None) #pobieramy kategorie z modelu i z niej pobieramy kategorie
            context = {
                'room_category': room.category,
                'form': AvalilabilityForm,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def get_context_data(self, **kwargs): #nie dziala
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_info(self, room_pk): #nie dziala
        room_info = Room.objects.all(self, room_pk)
        return room_info


    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)  # dlaczego kwargs
        room_list = Room.objects.filter(category=category)
        form = AvalilabilityForm(request.POST) #pobiera z post

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:  # jezeli True to dodajemy do avaialbe_rooms[]
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:  # jezeli jest cos na liscie czyli lista jest > 0
            room = available_rooms[0]  # dla pierwszego z listy wolnego pokoju towrzymy rezerwacje
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('this category of rooms are booked')

class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotelbooking:BookingList')# jezeli success_url to reverse_lazy jezlie w fukncji to reverse


# class BookingView(FormView): rezerwacja w oddzielnym formularzy z wyborem kategorii
#     form_class = AvalilabilityForm
#     template_name = 'availability_form.html'
#
#     def form_valid(self, form):
#         data = form.cleaned_data # pobieramy data z wypelnionego formularza
#         room_list = Room.objects.filter(category=data['room_category'])
#         available_rooms=[]
#         for room in room_list: #jezeli True to dodajemy do avaialbe_rooms[]
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_rooms.append(room)
#
#         if len(available_rooms)>0: #jezeli jest cos na liscie czyli lista jest > 0
#             room = available_rooms[0]# dla pierwszego z listy wolnego pokoju towrzymy rezerwacje
#             booking = Booking.objects.create(
#                 user = self.request.user,
#                 room = room,
#                 check_in = data['check_in'],
#                 check_out = data['check_out']
#             )
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse('this category of rooms are booked')

class CalendarView(ListView):
    model = Booking
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return datetime.today()