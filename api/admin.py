from django.contrib import admin
from .models import Matches, User, Location
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from image_cropping import ImageCroppingMixin


@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'teamSize', 'time', 'sport', 'owner', 'get_challenger', 'match_location')
    search_fields = ('id','teamSize', 'time','sport',  'owner', 'challenger', 'match_location')
    readonly_fields = ('opponentSize',)
    def get_challenger(self, obj):
        return  ", ".join([str(c.username) for c in obj.challenger.all()]) if obj.challenger.all() else "None"
class ChangeForm(ImageCroppingMixin, forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'height', 'weight', 'age','location_state', "location_city", 'user_picture')

class CustomUserAdmin(ImageCroppingMixin, UserAdmin):
    add_form = UserCreationForm
    form = ChangeForm
    model = User
    list_display = ['pk','username', 'first_name', 'last_name','location_state', "location_city", 'height', 'weight', 'age', 'user_picture']
    add_fieldsets = (
        (None, {'fields': ('username','first_name',  'last_name', 'password','location_state', "location_city", 'height', 'weight', 'age', 'user_picture')}),
    )
    fieldsets = add_fieldsets
admin.site.register(User, CustomUserAdmin)
admin.site.register(Location)


















