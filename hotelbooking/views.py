from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, FormView, View, DeleteView, DetailView
from .models import Room, Booking
from .forms import AvalilabilityForm
from hotelbooking.booking_funkctions.availibility import check_availability
from hotelbooking.booking_funkctions.get_room_cat_url_list import get_room_cat_url_list
from hotelbooking.booking_funkctions.get_room_category_human_format import get_room_category_human_format
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone



def home(request):
    # context = {}
    # context = cal_context(context)
    # return render(request, 'home.html', context)
    return render(request, 'home.html')

def success(request):


    return render(request, 'success.html')



def RoomListView(request):
    room_category_url_list = get_room_cat_url_list()
    context = {
        'room_list': room_category_url_list,
    }
    return render(request, 'room_list.html', context)

# def RoomListView(request): bez fuknkcji w booking functions
#         room = Room.objects.all()[0] #pobiera pierwszy losowy room object
#         room_categories = dict(room.ROOM_CATEGORIES)# tworzy slownik
#         room_values = room_categories.values()
#         room_list = []  # pusta lista category, URL
#
#         for room_category in room_categories:
#             room = room_categories.get(room_category) #room_category=value, category=key
#             room_url = reverse('hotelbooking:RoomDetailView', kwargs={'category': room_category})
#             room_list.append((room_category, room_url))
#         context = {
#             'room_list': room_list,
#         }
#         return render(request, 'room_list.html', context)

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
            if check_availability(room, data['check_in'].date(), data['check_out'].date()):
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
            # return HttpResponse(booking)

            return render(request, 'success_booking.html', {'booking':booking})
        else:
            return HttpResponse('this category of rooms are booked')



# class RoomDetailView(View): #tworzymy do zrezerwacji z formularzy POST Get
#     def get(self, request, *args, **kwargs):
#         category = self.kwargs.get('category', None) #dlaczego kwargs
#         human_format_room_category = get_room_category_human_format(category)
#         form = AvalilabilityForm()
#         if human_format_room_category is not None:
#             context = {
#                 'room_category': human_format_room_category,
#                 'form': form,
#             }
#             return render(request, 'room_detail_view.html', context)
#         else:
#             return HttpResponse('Category does not exist')
#
#     def post(self, request, *args, **kwargs):
#         category = self.kwargs.get('category', None)  # dlaczego kwargs
#         room_list = Room.objects.filter(category=category)
#         form = AvalilabilityForm(request.POST) #pobiera z post
#
#         if form.is_valid():
#             data = form.cleaned_data
#
#         available_rooms = []
#         for room in room_list:  # jezeli True to dodajemy do avaialbe_rooms[]
#             if check_availability(room, data['check_in'], data['check_out']):
#                 available_rooms.append(room)
#
#         if len(available_rooms) > 0:  # jezeli jest cos na liscie czyli lista jest > 0
#             room = available_rooms[0]  # dla pierwszego z listy wolnego pokoju towrzymy rezerwacje
#             booking = Booking.objects.create(
#                 user=self.request.user,
#                 room=room,
#                 check_in=data['check_in'],
#                 check_out=data['check_out']
#             )
#             booking.save()
#             return HttpResponse(booking)
#         else:
#             return HttpResponse('this category of rooms are booked')

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