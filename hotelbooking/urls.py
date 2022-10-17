from django.urls import path
from. views import RoomList, BookingList, BookingView
from . import views
app_name = 'hotelbooking'

urlpatterns = [
    path('', views.home, name='home'),
    path('room_list/', RoomList.as_view(), name='RoomList'),
    path('room_detail/<int:pk>', views.room_detail_view, name='room_detail.view'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    path('book/', BookingView.as_view(), name='booking_view')
]
