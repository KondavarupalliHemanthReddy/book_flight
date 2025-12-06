from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Booking

class FlightSearchForm(forms.Form):
    origin = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-field-custom pl-10',
            'placeholder': 'City or Airport',
            'id': 'from',
            'name': 'origin'
        }),
        label='From'
    )
    destination = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-field-custom pl-10',
            'placeholder': 'City or Airport',
            'id': 'to',
            'name': 'destination'
        }),
        label='To'
    )
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'input-field-custom pl-10',
            'type': 'date',
            'id': 'date',
            'name': 'departure_date'
        }),
        label='Departure Date'
    )
    passengers = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'input-field-custom pl-10',
            'id': 'passengers',
            'name': 'passengers',
            'value': '1',
            'min': '1'
        }),
        label='Passengers'
    )

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger_first_name', 'passenger_last_name', 'passenger_email', 'passenger_phone']
        widgets = {
            'passenger_first_name': forms.TextInput(attrs={
                'class': 'input-field-custom',
                'placeholder': 'John',
                'id': 'firstName'
            }),
            'passenger_last_name': forms.TextInput(attrs={
                'class': 'input-field-custom',
                'placeholder': 'Doe',
                'id': 'lastName'
            }),
            'passenger_email': forms.EmailInput(attrs={
                'class': 'input-field-custom',
                'placeholder': 'john.doe@example.com',
                'id': 'email'
            }),
            'passenger_phone': forms.TextInput(attrs={
                'class': 'input-field-custom',
                'placeholder': '+1 234 567 8900',
                'id': 'phone'
            }),
        }
        labels = {
            'passenger_first_name': 'First Name',
            'passenger_last_name': 'Last Name',
            'passenger_email': 'Email Address',
            'passenger_phone': 'Phone Number'
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-field-custom',
            'placeholder': 'Email or Username',
            'id': 'id_username',
            'autocomplete': 'username'
        }),
        label='Email or Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field-custom',
            'placeholder': '••••••••',
            'id': 'id_password',
            'autocomplete': 'current-password'
        }),
        label='Password'
    )

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input-field-custom',
            'placeholder': 'you@example.com',
            'id': 'id_email',
            'autocomplete': 'email'
        }),
        label='Email'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field-custom',
                'placeholder': 'johndoe',
                'id': 'id_username',
                'autocomplete': 'username'
            })
        }
        labels = {
            'username': 'Username'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'input-field-custom',
            'placeholder': '••••••••',
            'id': 'id_password1',
            'autocomplete': 'new-password'
        })
        self.fields['password1'].label = 'Password'
        
        self.fields['password2'].widget.attrs.update({
            'class': 'input-field-custom',
            'placeholder': '••••••••',
            'id': 'id_password2',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].label = 'Confirm Password'
        
        # Update help texts to be more user-friendly
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = 'Password must be at least 8 characters.'
        self.fields['password2'].help_text = None