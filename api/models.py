# from django.db import models

# Create your models here.
from django.db import models
from django import forms
# Create your models here.
# from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import related
from image_cropping import ImageRatioField, ImageCropField
import google_streetview.api
import googlemaps
import us

def get_location_image_url(location_name, location_city, location_state):
    place_name = f"{location_name} {location_city}, {location_state}" 
    API_KEY = "AIzaSyDGxpJcJahGs7qU6kqVsVKpo4Wr3Kw8F7o"

    params = [{
      'size': '200x300',
      'source': "outdoor",
      'location': place_name,
      'key': "AIzaSyDGxpJcJahGs7qU6kqVsVKpo4Wr3Kw8F7o"
    }]


    image_url = ""

    # Create a results object
    results = google_streetview.api.results(params)

    # Download images to directory 'downloads'
    try:
      results.preview()
      url_place = place_name.replace(" ", "%20")
      image_url = f"https://maps.googleapis.com/maps/api/streetview?size=600x600&location={url_place}&fov=120&source=outdoor&key=AIzaSyDGxpJcJahGs7qU6kqVsVKpo4Wr3Kw8F7o"
    except KeyError as error:
      gmaps = googlemaps.Client(API_KEY)
      
      place_result = gmaps.places(query = place_name, radius = 400)

      my_place_id = place_result["results"][0]["place_id"]

      my_fields = ['photo']

      place_details = gmaps.place(place_id = my_place_id, fields = my_fields)
      photo_id = place_details['result']['photos'][0]['photo_reference']
      pw = 400

      raw_image_data = gmaps.places_photo(photo_reference= photo_id, max_height = pw, max_width = pw)
      image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_id}&key=AIzaSyDGxpJcJahGs7qU6kqVsVKpo4Wr3Kw8F7o"
      
    return image_url


class User(AbstractUser):
    def upload_to(instance, filename):
        return 'staticfiles/%s/%s' % (instance.username, filename)

    height = models.CharField(max_length=4, null = False, blank = False)
    weight = models.IntegerField(null = False, blank = False)
    age = models.IntegerField(null = False, blank = False)
    user_picture = ImageCropField(null = False, blank = False, upload_to=upload_to)
    cropping = ImageRatioField('user_picture', '430x360')
    location_state = models.CharField(max_length=70, null=False, blank=False)
    location_city = models.CharField(max_length=70, null=False, blank=False)

    def __str__(self):
        return self.username
    
options = (
        ('basketball','Basketball'),
        ('soccer', 'Soccer'),
        ( 'football', 'Football'),
        ('tennis' ,'Tennis'),
        ('volleyball', 'VolleyBall'),
        ('frisbee', 'Frisbee')
    )

tSize = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11)
)

class Timezone(models.Model):
    timezone = models.CharField(max_length = 50)
    time = models.TimeField()

class Location(models.Model):
    location_name = models.CharField(max_length=100)
    location_address = models.CharField(max_length=300)
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=100)
    location_image_url = models.TextField(null = True, blank = True)
    matches_count = models.IntegerField(default = 0)
    timezone = models.CharField(max_length=50, blank=True, null = True)

    def __str__(self):
        return f'{self.location_name} - {self.location_address} - {self.location_city} - {self.location_state}'

    def save(self, *args, **kwargs):
        self.timezone = self.timezone
        self.location_image_url = get_location_image_url(self.location_name, self.location_city, self.location_state)
        return super().save(*args, **kwargs)


class Matches(models.Model):
    teamSize = models.IntegerField(null=True)
    opponentSize = models.IntegerField(null=True)
    sport  = models.CharField(max_length=15, choices=options, blank= False, null = False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches")    
    challenger = models.ManyToManyField(User, related_name="challenger", null=True, blank = True)    
    taken = models.BooleanField(default=False)
    time = models.TimeField()

    match_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name = "matches", null = True, blank = True)



    def save(self, *args, **kwargs):
        if not self.pk: 
            loc_count = self.match_location.matches.all().count() 
            print(loc_count)
            location = Location.objects.filter(pk = self.match_location.pk).update(matches_count = loc_count + 1) 
            
        if not self.opponentSize:
            self.opponentSize = self.teamSize

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.sport} {self.teamSize} vs. {self.opponentSize}'





