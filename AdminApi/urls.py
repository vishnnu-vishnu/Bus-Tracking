from django.urls import path
from AdminApi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter



router=DefaultRouter()
router.register("route",views.RouteView,basename="route")
router.register("ownerview",views.OwnersView,basename="ownerview")
router.register("passengerview",views.PassengerView,basename="ownerview")
router.register("bus",views.BusView,basename="bus-list")
router.register("assignedroutes",views.AssignedRoutesView,basename="assignedroutes")



urlpatterns = [
    path("register/",views.AdminCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token")

    
]+router.urls