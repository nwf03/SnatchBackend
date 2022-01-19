from rest_framework import serializers
from .models import Matches, User, Location


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'height', 'weight', 'age', 'user_picture']



class LocationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Location
        fields = ['id', 'location_name', 'location_address', 'location_city', 'location_state', 'location_image_url', 'matches_count']


class MatchSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    challenger = UserSerializer(many = True)
    match_location = LocationSerializer()
    time = serializers.TimeField(format="%-I:%M %p")
    class Meta:
        model = Matches
        fields= ['id',  'owner', 'challenger', 'sport', 'teamSize', 'opponentSize', 'time', 'taken', 'match_location']
    
class CreateLocationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Location
        fields = [ 'location_name', 'location_address', 'location_city', 'location_state', "timezone"]

    


class CreateMatchSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    match_location = CreateLocationSerializer()
    time = serializers.TimeField(format="%-I:%M %p")

    class Meta:
        model = Matches
        fields = ['id',  'owner', 'challenger', 'sport', 'teamSize', 'opponentSize', 'time', 'taken', 'match_location']

    def create(self, validated_data):
        location_data = validated_data.pop('match_location')
        location_name = location_data["location_name"]
        location_address = location_data["location_address"]
        location_city = location_data["location_city"]
        location_state = location_data["location_state"]
        timezone = location_data["timezone"]
        match_location = None

        challengers = validated_data.get("challenger") if validated_data.get("challenger") else None
        validated_data.pop("challenger")
        queryset = Location.objects.filter(location_name = location_name, location_address = location_address, location_city = location_city, location_state = location_state).exists()
        if not queryset:
            match_location = Location.objects.create(location_name = location_name, location_address = location_address, location_city = location_city, location_state = location_state, timezone = timezone )
        else:
            match_location = Location.objects.get(location_name = location_name, location_address = location_address, location_city = location_city, location_state = location_state)
        match = Matches.objects.create(match_location = match_location, **validated_data)
        if challengers:
            match.challenger.add(*challengers)
        return match



class EditMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matches
        fields = ['id',  'owner', 'challenger', 'sport', 'teamSize', 'opponentSize', 'time', 'taken', 'match_location']

class LoggedInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','location_state', "location_city", 'height', 'weight', 'age', 'user_picture']

