from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Check POST request for validity and save if valid. If invalid, route to add new places form
def place_list(request):
    if request.method == 'POST': # If POST continue and check for validity
        form = NewPlaceForm(request.POST)
        place = form.save() # Create a new place
        if form.is_valid: # Confirm constraint requirements met
            place.save() # Save new place to DB
            return redirect('place_list') # Redirect to GET view via place_list

    places = Place.objects.filter(visited=False).order_by('name') # If not POST, render new places form
    new_place_form = NewPlaceForm() # Assign variable to NewPlaceForm to include in tuple below
    return render(request, 'travel_wishlist/wishlist.html' , {'places' : places , 'new_place_form' : new_place_form}) # Retrns form for place to be added to wishlist

def places_visited(request): # Renders visited places
    visited = Place.objects.filter(visited=True).order_by('name') # Determine visited places
    return render(request, 'travel_wishlist/visited.html', {'visited' : visited}) # Return visited places

def place_was_visited(request, place_pk): # Searches for a visited place via pk/id
    if request.method == 'POST': # If POST, continue and check for validity
        place = get_object_or_404(Place , pk=place_pk) # If pk/id found, contine if not 404 error
        place.visited = True # If found by pk/id ...
        place.save() # Save visited place to db
    
    return redirect('place_list') # Redirect to GET view via place_list

def about(request): # Provides basic information about site and author
    author = 'Michael Lynch' # Author's name
    about = 'A website to create list of places to visit.' # About info 
    return render(request , 'travel_wishlist/about.html' , {'author' : author , 'about' : about}) # Renders for user
