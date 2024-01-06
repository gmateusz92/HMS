from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Booking
from datetime import date


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None,bookings=None, room_number=None):
		self.year = year
		self.month = month
		self.bookings = bookings
		self.room_number = room_number
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, bookings):
		booking_per_day = bookings.filter(check_in__day__lte=day, check_out__day__gte=day)

		d = ''
		for booking in booking_per_day:
			d += f'<div class="reservation" style="background-color: red;">Pokój {booking.room.number} zarezerwowany</div>'

		if day != 0:
			return f"<td><span class='date'>{day}  </span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	def formatmonth(self, withyear=True):
		bookings = Booking.objects.filter(check_in__year=self.year, check_out__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, bookings)}\n'
		return cal
	


# class Calendar(HTMLCalendar):
#     def __init__(self, year=None, month=None, bookings=None):
#         self.year = year
#         self.month = month
#         self.bookings = bookings
#         super(Calendar, self).__init__()

#     def formatday(self, day, bookings, room_number):
#         booking_per_day = bookings.filter(
#             check_in__day__lte=day,
#             check_out__day__gte=day,
#             room__number=room_number
#         )

#         d = ''
#         for booking in booking_per_day:
#             d += f'<div class="reservation" style="background-color: red;">Pokój {booking.room.number} zarezerwowany</div>'

#         if day != 0:
#             return f"<td><span class='date'>{day}  </span><ul> {d} </ul></td>"
#         return '<td></td>'

#     def formatweek(self, theweek, room_number):
#         week = ''
#         for d, weekday in theweek:
#             week += self.formatday(d, self.bookings, room_number)
#         return f'<tr> {week} </tr>'

#     # Poprawiony kod
# def formatmonth(self, withyear=True):
#     if hasattr(self, 'room_number') and self.room_number is not None:
#         bookings = self.bookings.filter(room__number=self.room_number, check_in__year=self.year, check_out__month=self.month)
#     else:
#         bookings = self.bookings.filter(check_in__year=self.year, check_out__month=self.month)

#     cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
#     cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
#     cal += f'{self.formatweekheader()}\n'
#     for week in self.monthdays2calendar(self.year, self.month):
#         cal += f'{self.formatweek(week, bookings)}\n'
#     return cal

