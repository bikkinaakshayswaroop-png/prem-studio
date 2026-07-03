from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'full_name',
            'phone',
            'email',
            'event_type',
            'event_date',
            'location',
            'message',
        ]

        widgets = {

            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),

            'event_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Location'
            }),

            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us about your event'
            }),
        }
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "profile_photo",
            "phone",
            "address",
        ]
        
from django import forms
from .models import Gallery

class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = [
    "album_name",
    "title",
    "image",
    ]

        widgets = {
            "user": forms.Select(attrs={
                "class": "form-control"
            }),

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Album Title"
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }