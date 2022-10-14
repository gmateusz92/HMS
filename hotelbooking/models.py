from django.db import models
from django.conf import settings


class Room(models.Model):
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    number = models.IntegerField(null=True)
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES, null=True)
    beds = models.IntegerField(null=True)
    capacity = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.number} {self.category} with {self.beds} beds for {self.capacity} people'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in}'
