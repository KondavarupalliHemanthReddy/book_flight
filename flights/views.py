from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Flight, Booking, Seat, Airport
from .forms import FlightSearchForm, BookingForm, CustomLoginForm, CustomSignupForm
from decimal import Decimal 
def home(request):
    form = FlightSearchForm()
    context = {
        'form': form,
        'page': 'home'
    }
    return render(request, 'home.html', context)

# def search_flights(request):
    flights = []
    form = FlightSearchForm()
    
    if request.method == 'GET' and 'origin' in request.GET:
        form = FlightSearchForm(request.GET)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            departure_date = form.cleaned_data['departure_date']
            passengers = form.cleaned_data['passengers']
            
            # Search flights
            flights = Flight.objects.filter(
                Q(origin__city__icontains=origin) | Q(origin__code__icontains=origin),
                Q(destination__city__icontains=destination) | Q(destination__code__icontains=destination),
                departure_time__date=departure_date,
                available_seats__gte=passengers
            ).select_related('airline', 'origin', 'destination')
            
            # Store search params in session
            request.session['search_params'] = {
                'origin': origin,
                'destination': destination,
                'departure_date': str(departure_date),
                'passengers': passengers
            }
    
    context = {
        'flights': flights,
        'form': form,
        'page': 'searchResults'
    }
    return render(request, 'search_results.html', context)
def search_flights(request):
    flights = []
    form = FlightSearchForm()

    if request.method == 'GET' and 'origin' in request.GET:
        form = FlightSearchForm(request.GET)
        if form.is_valid():
            origin_name = form.cleaned_data['origin']
            destination_name = form.cleaned_data['destination']
            departure_date = form.cleaned_data['departure_date']
            passengers = form.cleaned_data['passengers']

            # Find airport IDs by city or code
            origin_airports = Airport.objects.filter(
                Q(city__icontains=origin_name) | Q(code__icontains=origin_name)
            )
            destination_airports = Airport.objects.filter(
                Q(city__icontains=destination_name) | Q(code__icontains=destination_name)
            )

            # Filter flights using airport IDs
            flights = Flight.objects.filter(
                origin__in=origin_airports,
                destination__in=destination_airports,
                departure_time__date=departure_date,
                available_seats__gte=passengers
            ).select_related('airline', 'origin', 'destination')

            # Store search params in session
            request.session['search_params'] = {
                'origin': origin_name,
                'destination': destination_name,
                'departure_date': str(departure_date),
                'passengers': passengers
            }

    context = {
        'flights': flights,
        'form': form,
        'page': 'searchResults'
    }
    return render(request, 'search_results.html', context)
@login_required
def booking_page(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    # seats = Seat.objects.filter(flight=flight)
    seats = Seat.objects.filter(flight=flight).order_by('seat_number')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        seat_number = request.POST.get('seat_number')
        
        if form.is_valid() and seat_number:
            seat = get_object_or_404(Seat, flight=flight, seat_number=seat_number, status='available')
            
            # Create booking
            booking = form.save(commit=False)
            booking.user = request.user
            booking.flight = flight
            booking.seat = seat
            booking.total_price = flight.base_price + Decimal('45.50')
            booking.status = 'confirmed'
            booking.save()
            
            # Update seat status
            seat.status = 'occupied'
            seat.save()
            
            # Update available seats
            flight.available_seats -= 1
            flight.save()
            
            # messages.success(request, 'Booking Confirmed! Check your email for details.')
            return redirect('dashboard')
    else:
        form = BookingForm()
    
    context = {
        'flight': flight,
        'seats': seats,
        'form': form,
        'page': 'booking'
    }
    return render(request, 'booking.html', context)


@login_required
def dashboard(request):
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        status='confirmed',
        flight__departure_time__gte=timezone.now()
    ).select_related('flight', 'flight__airline', 'flight__origin', 'flight__destination', 'seat')
    
    past_bookings = Booking.objects.filter(
        user=request.user,
        flight__departure_time__lt=timezone.now()
    ).select_related('flight', 'flight__airline', 'flight__origin', 'flight__destination', 'seat')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'page': 'dashboard'
    }
    return render(request, 'dashboard.html', context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.save()
        
        # Free up the seat
        booking.seat.status = 'available'
        booking.seat.save()
        
        # Update available seats
        booking.flight.available_seats += 1
        booking.flight.save()
        
        # messages.success(request, 'Booking cancelled successfully.')
    
    return redirect('dashboard')

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful! Welcome back.')
            return redirect('home')
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')

def user_signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomSignupForm()
    
    return render(request, 'signup.html', {'form': form})