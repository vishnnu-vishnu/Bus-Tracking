from django.urls import path
from BusOwner import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter



router=DefaultRouter()
router.register("bus",views.BusView,basename="bus-add")  
router.register("busdriver",views.BusDriverView,basename="busdriver-add")  
router.register("routes",views.RouteView,basename="route-list")
router.register("assignedroutes",views.RouteAssignsView,basename="assignedroutes-list")

 







urlpatterns = [
    path("register/",views.OwnerCreationView.as_view(),name="signup"),
    path("token/",views.CustomObtainAuthToken.as_view(),name="token"),
    path('fuel_stations/', views.FuelstationView.as_view()),
    path('workshop/', views.WorkshopView.as_view()),


    
]+router.urls