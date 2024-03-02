from django.shortcuts import render
from rest_framework.views import APIView,status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions

from Passesnger.serializers import PassengerSerializer,AssignedRoutesSerializer,RouteSerializer,BusstopSerializer
from AdminApi.models import Passenger,Route,RouteAssign



# Create your views here.


class PassengerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=PassengerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Passenger")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        
class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = RouteSerializer
        
    def list(self,request,*args,**kwargs):
        qs=Route.objects.all()
        serializer=RouteSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            route = Route.objects.get(pk=kwargs.get("pk"))
        except Route.DoesNotExist:
            return Response({"error": "Route does not exist"},status=status.HTTP_404_NOT_FOUND)
        route_serializer = RouteSerializer(route)
        stops_serializer = BusstopSerializer(route.busstop_set.all(), many=True)
        bus_serializer = AssignedRoutesSerializer(route.routeassign_set.all(), many=True)
        response_data = route_serializer.data
        response_data['bus assigned'] = bus_serializer.data
        response_data['stops'] = stops_serializer.data
        return Response(response_data)
    