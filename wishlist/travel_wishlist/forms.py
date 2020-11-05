from django import forms
from .models import Place # Import Place from models.py

class NewPlaceForm(forms.ModelForm): # Create a New Place form
    class Meta:
        model = Place # Assign variable name "model" and call Place class
        fields = ('name' , 'visited') # Designates two fields for the desired information: place and whether or not visited
