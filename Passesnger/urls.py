from django.urls import path
from Passesnger import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("route",views.RouteView,basename="route")


urlpatterns = [
    path("register/",views.PassengerCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    path("alert/",views.AlertMessageView.as_view(),name="alert"),
    path('bus_stations/', views.BusStationView.as_view()),
    path('fuel_stations/', views.FuelstationView.as_view()),
    path('workshop/', views.WorkshopView.as_view()),

    
] + router.urls