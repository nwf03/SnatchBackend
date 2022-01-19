
from django.forms.models import model_to_dict
from .serializers import CreateUserSerializer, CreateLocationSerializer, MatchSerializer, EditMatchSerializer, UserSerializer, LoggedInUserSerializer, CreateMatchSerializer, LocationSerializer
from rest_framework import viewsets, permissions, generics, filters, serializers
from .models import Location, Matches, User
import django_filters.rest_framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

# Create your views here.

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CreateUser(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = []

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data["username"])
            refresh = RefreshToken.for_user(user)

            response_dict = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                }
            for field, val in serializer.data.items():
                response_dict[field] = val
            response_dict["current_match"] = None
            
            return Response(response_dict, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.pk == request.user.pk

class LocationSearch(generics.ListAPIView):
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["location_name", "location_address", "location_city", "location_state"]
    search_fileds = ["^location_name", "^location_address"]
    def get_queryset(self):
        user = self.request.user
        return Location.objects.filter(location_state = user.location_state, location_city = user.location_city)



class ListMatches(generics.ListAPIView):
    queryset = Matches.objects.all().filter(taken=False)

    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['owner', 'challenger','sport', 'teamSize', 'match_location__location_city', 'match_location__location_state']


class ViewEditMatches(generics.RetrieveUpdateDestroyAPIView):
    queryset = Matches.objects.all()
    serializer_class = EditMatchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListUsers(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username = username)
        return queryset


class ViewEditUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


class ListLoggedInUser(generics.ListCreateAPIView):
    serializer_class = LoggedInUserSerializer
    queryset = User.objects.all()
    permissions = [permissions.IsAuthenticated]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        d = []
        url = "https://opm-backend.herokuapp.com/" 
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # Add extra responses here  
        data['user_id'] = self.user.id
        data['username'] = self.user.username

        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['age'] = self.user.age
        data['weight'] = self.user.weight
        data['height'] = self.user.height 
        data['user_picture'] = f"{url}{str(self.user.user_picture)}" if self.user.user_picture != None else ""
        data["current_match"] = None
        match = None
        
        if self.user.matches.all().count() > 0:
            match = self.user.matches.all()[0]
            challenger = []
            for opp in match.challenger.all():
                user = {"id": opp.id, "username": opp.username, "first_name": opp.first_name, "last_name": opp.last_name, "height": opp.height, "weight": opp.weight, "age": opp.age, "user_picture": f"{url}{str(opp.user_picture)}"}
                challenger.append(user)
                
            md = {"id": match.id, "owner": {"id": match.owner.id, "username": match.owner.username, "first_name":  match.owner.first_name, "last_name": match.owner.last_name,
                "height": match.owner.height, "weight": match.owner.weight, "age": match.owner.age, "user_picture": f"{url}{str(match.owner.user_picture)}"},
                "challenger": challenger, "sport": match.sport, "teamSize": match.teamSize, 'opponentSize': match.opponentSize, "time": match.time.strftime("%I:%M %p"), "taken": match.taken, "match_location": model_to_dict(match.match_location)}
            data['current_match'] = md
        else:   
            for match in self.user.challenger.all():
                challenger = []
                for opp in match.challenger.all():
                    user = {"id": opp.id, "username": opp.username, "first_name": opp.first_name, "last_name": opp.last_name, "height": opp.height, "weight": opp.weight, "age": opp.age, "user_picture": f"{url}{str(opp.user_picture)}"}
                    challenger.append(user)
                md = {"id": match.id, "owner": {"id": match.owner.id, "username": match.owner.username, "first_name":  match.owner.first_name, "last_name": match.owner.last_name,
                "height": match.owner.height, "weight": match.owner.weight, "age": match.owner.age, "user_picture": f"{url}{str(match.owner.user_picture)}"},
                "challenger": challenger, "sport": match.sport, "teamSize": match.teamSize, 'opponentSize': match.opponentSize, "time": match.time.strftime("%I:%M %p"), "taken": match.taken, "match_location": model_to_dict(match.match_location)}
                data['current_match'] = md

        d.append(data)
        return d


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    queryset = MyTokenObtainPairSerializer


class CreateLocation(generics.CreateAPIView):
    serializer_class = CreateLocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateMatch(generics.CreateAPIView):
    serializer_class = CreateMatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        url = "https://opm-backend.herokuapp.com/"
        self.request.POST._mutable = True
        new_data = request.data
        print(request.data)
        res_data = new_data
        user = User.objects.get(username=res_data["owner"])
        user_data = {"id": user.id, "username": user.username, "first_name": user.first_name, "last_name": user.last_name,
                    "height": user.height, "weight": user.weight, "age": user.age, "user_picture": f'{url}{str(user.user_picture)}'}
        serializer = CreateMatchSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            print(f'{res_data["owner"]} username gang')
            res_data["id"] = serializer.data["id"]
            res_data["owner"] = user_data
            location = Location.objects.get(location_name = serializer.data["match_location"]["location_name"],location_address = serializer.data["match_location"]["location_address"], location_city = serializer.data["match_location"]["location_city"], location_state = serializer.data["match_location"]["location_state"])
            response_dict = serializer.data
            response_dict["owner"] = user_data
            response_dict["match_location"] = {
                "id": 6,
                "location_name": location.location_name,
                "location_address": location.location_address,
                "location_city":    location.location_city,
                "location_state": location.location_state,
                "location_image_url": location.location_image_url,
                "matches_count": location.matches_count
            }
            return Response(response_dict, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeData(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @staticmethod
    def get(request):
        user_count = User.objects.all().count()

        if len(request.query_params) < 2 or ("state" not in request.query_params or "city" not in request.query_params):
            return Response({
                "error": "please provide state and city in url query params"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            location_state = request.query_params["state"]
            location_city = request.query_params["city"]

        match_count = Matches.objects.filter(match_location__location_city = location_city, match_location__location_state = location_state).count()
        basketball_matches = Matches.objects.all().filter(sport="basketball", match_location__location_city = location_city, match_location__location_state = location_state).count()
        soccer_matches = Matches.objects.all().filter(sport="soccer", match_location__location_city = location_city, match_location__location_state = location_state).count()
        football_matches = Matches.objects.all().filter(sport="football", match_location__location_city = location_city, match_location__location_state = location_state).count()
        volleyball_matches = Matches.objects.all().filter(sport="volleyball", match_location__location_city = location_city,  match_location__location_state = location_state).count()
        tennis_matches = Matches.objects.all().filter(sport="tennis", match_location__location_city = location_city, match_location__location_state = location_state).count()
        team_count = [Matches.objects.all().filter(teamSize=i, match_location__location_city = location_city, match_location__location_state = location_state).count() for i in range(1,14)]
        matches_location = Location.objects.filter(location_city = location_city, location_state = location_state)
        popular_locations_data = matches_location.order_by("-matches_count")[:10]
        popular_locations = LocationSerializer(popular_locations_data, many=True, read_only=True)

        return Response({
            "counts":
                {
                    "user_count": user_count,
                    "All": match_count,
                    "Basketball": basketball_matches,
                    "Soccer": soccer_matches,
                    "Football": football_matches,
                    "Volleyball": volleyball_matches,
                    "Tennis": tennis_matches
                },
            "team_match_count": team_count,
            "popular_locations": popular_locations.data
            })






