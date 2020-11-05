from django.db import models

class Place(models.Model): # Create model
    name = models.CharField(max_length=200) # Set character limit for place name
    visited = models.BooleanField(default=False) # Default all places to not yet visited

    def __str__(self):
        return f'{self.name}, visited? {self.visited}' # Display place name and ask if visited
