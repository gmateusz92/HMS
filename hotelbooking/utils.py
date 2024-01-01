from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Booking
from datetime import date


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None,bookings=None):
		self.year = year
		self.month = month
		self.bookings = bookings
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, bookings):
		booking_per_day = bookings.filter(check_in__day__lte=day, check_out__day__gte=day)
		#event_end = events.filter(end_time__day=day)

		# time_range = DateTimeRange(start_datetime=day, end_datetime=day)
		# for value in time_range.range(datetime.timedelta(days=1)):
		# 	print(value)

		d = ''
		for booking in booking_per_day:
			d += f'<div class="reservation" style="background-color: red;">Pokój {booking.room.number} zarezerwowany</div>'


		# d = '<ul>'
		# for booking in booking_per_day:
		# 	d += f'   room {booking.room.number} reserved'
		# d +='<ul>'

		# if events_per_day == event_end:
		# 	for event in event_end:
		# 		d += f'<li> {event.title} {event.description} </li>'

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
	# filter events by year and month
	def formatmonth(self, withyear=True):
		bookings = Booking.objects.filter(check_in__year=self.year, check_out__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, bookings)}\n'
		return cal
	

# from datetime import datetime, timedelta
# from calendar import HTMLCalendar
# from .models import Booking
# from datetime import date

# class Calendar(HTMLCalendar):
#     def __init__(self, year=None, month=None):
#         self.year = year
#         self.month = month
#         super(Calendar, self).__init__()

#     def formatday(self, day, bookings):
#         booking_per_day = bookings.filter(check_in__day__lte=day, check_out__day__gte=day)

#         css_class = ''
#         for booking in booking_per_day:
#             css_class += ' reserved'
            
#         if day != 0:
#             return f"<td class='{css_class}'><span class='date'>{day}</span></td>"
#         return '<td></td>'

#     def formatweek(self, theweek, events):
#         week = ''
#         for d, weekday in theweek:
#             week += self.formatday(d, events)
#         return f'<tr> {week} </tr>'

#     def formatmonth(self, withyear=True):
#         bookings = Booking.objects.filter(check_in__year=self.year, check_out__month=self.month)

#         cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
#         cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
#         cal += f'{self.formatweekheader()}\n'
#         for week in self.monthdays2calendar(self.year, self.month):
#             cal += f'{self.formatweek(week, bookings)}\n'
#         return cal
