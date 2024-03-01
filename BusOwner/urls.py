from django.urls import path
from BusOwner import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter



router=DefaultRouter()
# router.register("place",views.PlaceCreate,basename="place")  
# router.register("routes",views.RouteViewSet,basename="routes")  
# router.register("busstop",views.BusStopViewSet,basename="busstop")  







urlpatterns = [
    path("register/",views.OwnerCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token")

    
]+router.urls