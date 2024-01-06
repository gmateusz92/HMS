from django.urls import path
from. views import RoomListView, BookingList, RoomDetailView, CancelBookingView, CalendarView #BookingView,

from . import views
app_name = 'hotelbooking'

urlpatterns = [
    path('', views.home, name='home'),
    path('success/', views.success, name='success'),
    path('room_list/', views.RoomListView, name='RoomList'),
    #path('<int:room_pk>/', views.room_detail_view, name='room_detail_view'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    #path('book/', BookingView.as_view(), name='BookingView'),
    path('room/<category>/', RoomDetailView.as_view(), name='room_detail'),
    #path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    #path("<int:year>/<str:month>/", views.home, name="home"),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('calendar/<int:room_id>/', views.CalendarView.as_view(), name='calendar'),
]
