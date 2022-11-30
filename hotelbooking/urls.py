from django.urls import path
from. views import RoomListView, BookingList, RoomDetailView, CancelBookingView #BookingView

from . import views
app_name = 'hotelbooking'

urlpatterns = [
    path('', views.home, name='home'),
    #path('room_list/', RoomListView.as_view(), name='RoomList'),
    path('room_list/', views.RoomListView, name='RoomList'),
    #path('<int:room_pk>/', views.room_detail_view, name='room_detail_view'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    #path('book/', BookingView.as_view(), name='BookingView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    #path("<int:year>/<str:month>/", views.home, name="home"),
path('calendar/', views.CalendarView.as_view(), name='calendar'),
]
