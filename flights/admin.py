from django.contrib import admin
from .models import Airline, Airport, Flight, Seat, Booking

# ------------------------------
# Airline Admin
# ------------------------------
@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


# ------------------------------
# Airport Admin
# ------------------------------
@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'code')
    list_filter = ('country', 'city')
    search_fields = ('name', 'city', 'country', 'code')


# ------------------------------
# Flight Admin
# ------------------------------
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'available_seats', 'total_seats', 'is_available')
    list_filter = ('airline', 'origin', 'destination', 'departure_time')
    search_fields = ('flight_number', 'origin__code', 'destination__code', 'airline__name')
    ordering = ('departure_time',)

    # show availability as a boolean
    def is_available(self, obj):
        return obj.available_seats > 0
    is_available.boolean = True
    is_available.short_description = 'Seats Available'


# ------------------------------
# Seat Admin
# ------------------------------
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('flight', 'seat_number', 'status')
    list_filter = ('status', 'flight')
    search_fields = ('seat_number', 'flight__flight_number')


# ------------------------------
# Booking Admin
# ------------------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'flight', 'seat', 'passenger_full_name', 'status', 'total_price', 'booking_date')
    list_filter = ('status', 'booking_date', 'flight__airline')
    search_fields = ('user__username', 'flight__flight_number', 'seat__seat_number', 'passenger_first_name', 'passenger_last_name')
    ordering = ('-booking_date',)

    # show full passenger name
    def passenger_full_name(self, obj):
        return f"{obj.passenger_first_name} {obj.passenger_last_name}"
    passenger_full_name.short_description = 'Passenger Name'
