from django.test import TestCase
from django.urls import reverse

from .models import Place

# Tests that an empty wishlist returns a message
class TestHomePage(TestCase):

    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list') # Get url via reverse pull
        response = self.client.get(home_page_url) # Get response from url
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # Confirm functional, valid response
        
        self.assertContains(response, 'You have no places in your wishlist.') # Display message if confirmed empty

# Tests to confirm the wishlist contains only not yet visited places
class TestWishlist(TestCase):

    fixtures = ['test_places'] # Create fixtures variable for test_places list

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list')) # Get response from url
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # Confirm functional, valid response

        self.assertContains(response, 'Tokyo') # Confirm does contain place
        self.assertContains(response, 'New York') # Confirm does contain place

        self.assertNotContains(response, 'San Francisco') # Confirm does not contain place
        self.assertNotContains(response, 'Moab') # Confirm does not contain place

# Tests for user message for empty visited places db
class TestVisitedPage(TestCase):

    def test_visited_page_shows_emptly_list_message_for_empty_database(self):
        response = self.client.get(reverse('places_visited')) # Get response from url
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html') # Confirm functional, valid response

        self.assertContains(response, 'You have not yet visited any places.') # Display message if confirmed empty

# Tests to confirm visited list contains only visited places
class VisitedList(TestCase):

    fixtures = ['test_places'] # Create fixtures variable for test_places list

    def test_visited_list_shows_visited_places(self):
        response = self.client.get(reverse('places_visited')) # Get response from url
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html') # Confirm functional, valid response

        self.assertContains(response, 'San Francisco') # Confirm does contain place
        self.assertContains(response, 'Moab') # Confirm does contain place

        self.assertNotContains(response, 'Tokyo') # Confirm does not contain place
        self.assertNotContains(response, 'New York') # Confirm does not contain place

# Tests to confirm new place is correctly being added to place_list
class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place_to_wishlist(self):
        add_place_url = reverse('place_list') # Get response from url
        new_place_data = {'name' : 'Tokyo' , 'visited' : False} # New test data to be added to place_list
        
        response = self.client.post(add_place_url, new_place_data, follow=True) # Get updated response

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # Confirm functional, valid response

        response_places = response.context['places'] # Gets info from places list
        self.assertEqual(1, len(response_places)) # Confirms places length at least one
        tokyo_from_response = response_places[0] # test place does not appear in list, not visited

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False) # Confirm test place not visited

        self.assertEqual(tokyo_from_database, tokyo_from_response) # Confirms both test and actual reflect not visited

# Tests to confirm visited places via pk/id
class TestVisitPlace(TestCase):

    fixtures = ['test_places'] # Create fixtures variable for test_places list

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, )) # Get response from url
        response = self.client.post(visit_place_url , follow=True) # Confirm functional, valid response

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # Return wishlist
        self.assertNotContains(response, 'New York') # Confirm place not found in wishlist

        new_york = Place.objects.get(pk=2) # Locate place via pk/id
        self.assertTrue(new_york.visited) # Confirm place was visited

# Test to confirm there are no non-existent places in the database
    def test_non_existent_place(self):
        visit_non_existent_place_url = reverse('place_was_visited' , args=(123456, )) # Get url response using non-existent data
        response = self.client.post(visit_non_existent_place_url , follow=True) # If non-existent data is not in database ...
        self.assertEqual(404, response.status_code) # Confirm a 404 error is generated
