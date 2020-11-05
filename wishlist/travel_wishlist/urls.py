from django.urls import path
from . import views

urlpatterns = [
    path('' , views.place_list , name='place_list'), # Creates a path to the url for  updating wishlist places
    path('visited' , views.places_visited , name='places_visited'), # Creates a path to the url for  visited.html
    path('place/<int:place_pk>/was_visited' , views.place_was_visited , name='place_was_visited'), # Creates a path to the url for updating visited places
    path('about' , views.about , name='about') # Creates a path to the url for about.html
]
