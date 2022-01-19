from django.urls import path
from .views import CreateUser, LocationSearch, ListMatches, ViewEditMatches, ListUsers, ViewEditUser, ListLoggedInUser, MyTokenObtainPairView, CreateMatch, HomeData, CreateLocation
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('create_location/', CreateLocation.as_view()),
    path('create_user/', CreateUser.as_view()),
    path('home/', HomeData.as_view()),
    path('matches/', ListMatches.as_view()),
    path('matches/create/', CreateMatch.as_view()),
    path('matches/<int:pk>/', ViewEditMatches.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', ListUsers.as_view(), name='users'),
    path('users/<int:pk>', ViewEditUser.as_view(), name='edit_user'),
    path('loggedUser/', ListLoggedInUser.as_view()),
    path('locations', LocationSearch.as_view())
]

