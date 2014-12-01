from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Well


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active')


class WellForm(forms.Form):
    """ Form to parse and validate well pk passed as
    GET argument. """
    well = forms.ModelChoiceField(queryset=Well.objects.all())
    
