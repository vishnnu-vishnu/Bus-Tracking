from django.urls import path
from Passesnger import views
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path("register/",views.PassengerCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token")

    
]