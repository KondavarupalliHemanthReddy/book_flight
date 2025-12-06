from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(upload_to='airline_logos/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Flight(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=20, unique=True)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    available_seats = models.IntegerField(validators=[MinValueValidator(0)])
    total_seats = models.IntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        ordering = ['departure_time']
    
    def __str__(self):
        return f"{self.flight_number}: {self.origin.code} → {self.destination.code}"
    
    @property
    def duration(self):
        delta = self.arrival_time - self.departure_time
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    
    @property
    def is_available(self):
        return self.available_seats > 0

class Seat(models.Model):
    SEAT_STATUS = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('selected', 'Selected'),
    )
    
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    status = models.CharField(max_length=10, choices=SEAT_STATUS, default='available')
    
    class Meta:
        unique_together = ('flight', 'seat_number')
    
    def __str__(self):
        return f"{self.flight.flight_number} - Seat {self.seat_number}"

class Booking(models.Model):
    BOOKING_STATUS = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    passenger_first_name = models.CharField(max_length=100)
    passenger_last_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    passenger_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.flight.flight_number}"