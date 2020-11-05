from django.contrib import admin
from .models import Place # Import Place class from models.py

admin.site.register(Place) # Grant admin access to Place
