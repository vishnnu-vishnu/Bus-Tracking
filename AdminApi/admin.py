from django.contrib import admin
from AdminApi.models import Busstop,Route,RouteAssign,CustomUser,BusOwner
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin panel
    list_display = ['username', 'email', 'user_type']
    # Add any other customizations as needed

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Busstop)
admin.site.register(BusOwner)
admin.site.register(RouteAssign)
admin.site.register(Route)