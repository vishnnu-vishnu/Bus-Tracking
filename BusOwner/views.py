from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


from rest_framework.views import APIView,status
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response

from BusOwner.serializers import OwnerSerializer,BusSerializer,BusDriverSerializer,RouteAssignSerializer,RouteSerializer,BusstopSerializer,RouteAssignedSerializer
from AdminApi.models import Busstop,BusOwner,Route,Bus,BusDriver,RouteAssign
from Passesnger.services import get_coordinates,get_workshops,get_fuel_stations

# Create your views here.

# custom permission view
class IsBusOwnerApproved(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'busowner'):
            return request.user.busowner.is_approved
        return False    

class OwnerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Bus Owner")
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)


class BusView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]
    
    def create(self,request,*args,**kwargs):
        serializer=BusSerializer(data=request.data)
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        if serializer.is_valid():
            serializer.save(busowner=busowner_obj)
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)
            
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=Bus.objects.filter(busowner=busowner_obj)
        serializer=BusSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Bus.objects.get(id=id)
        serializer=BusSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Bus.objects.get(id=id)
            instance.delete()
            return Response({'status':1,"msg": "bus removed"})
        except Bus.DoesNotExist:
            return Response({'status':0,"msg": "bus not found"}, status=status.HTTP_404_NOT_FOUND)
  

class BusDriverView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]
    
    def create(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        serializer=BusDriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(busowner=busowner_obj)
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=BusDriver.objects.filter(busowner=busowner_obj)
        serializer=BusDriverSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BusDriver.objects.get(id=id)
        serializer=BusDriverSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =BusDriver.objects.get(id=id)
            instance.delete()
            return Response({'status':1,"msg": "Bus Driver removed"})
        except BusDriver.DoesNotExist:
            return Response({'status':0,"msg": "Bus Driver not found"}, status=status.HTTP_404_NOT_FOUND)    



class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]
    
    def list(self,request,*args,**kwargs):
        qs=Route.objects.all()
        serializer=RouteSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self, request, *args, **kwargs):
        try:
            route = Route.objects.get(pk=kwargs.get("pk"))
        except Route.DoesNotExist:
            return Response({"error": "Route does not exist"},status=status.HTTP_404_NOT_FOUND)
        route_serializer = RouteSerializer(route)
        stops_serializer = BusstopSerializer(route.busstop_set.all(), many=True)
        response_data = route_serializer.data
        response_data['stops'] = stops_serializer.data
        return Response(data={'status':1,'data':response_data})
    
    
    @action(methods=["post"], detail=True)
    def my_buses(self,request,*args,**kwargs):
        route_id = kwargs.get("pk")
        route_obj = Route.objects.get(id=route_id)
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=RouteAssign.objects.filter(busowner=busowner_obj,route=route_obj)
        serializer=RouteAssignedSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    

    @action(methods=["post"], detail=True)
    def route_assign(self, request, *args, **kwargs):
        serializer = RouteAssignSerializer(data=request.data)
        route_id = kwargs.get("pk")
        route_obj = Route.objects.get(id=route_id)
        busowner_id = request.user.id
        busowner_obj = BusOwner.objects.get(id=busowner_id)

        if serializer.is_valid():
            start_time = serializer.validated_data.get('start_time')
            busdriver=serializer.validated_data.get('busdriver')
            end_time = serializer.validated_data.get('end_time')
            existing_assignments = RouteAssign.objects.filter(route=route_obj, start_time=start_time, end_time=end_time,busdriver=busdriver).exists()
            if existing_assignments:
                return Response(data={'status': 0, 'msg': 'A bus is already assigned to the route during the same time period'}, status=status.HTTP_400_BAD_REQUEST)

            # bus_id = serializer.validated_data.get('bus')
            # bus_obj = Bus.objects.get(id=bus_id)
            # bus_obj.is_active = True
            # bus_obj.save()
            serializer.save(route=route_obj, busowner=busowner_obj)
            return Response(data={'status': 1, 'data': serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status': 0, 'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)    
    

class RouteAssignsView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,IsBusOwnerApproved]
    
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=RouteAssign.objects.filter(busowner=busowner_obj)
        serializer=RouteAssignedSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
     
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=RouteAssign.objects.get(id=id)
        serializer=RouteAssignedSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})  
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =RouteAssign.objects.get(id=id)
            instance.delete()
            return Response({'status':1,"msg": "RouteAssign Driver removed"})
        except BusDriver.DoesNotExist:
            return Response({'status':0,"msg": "RouteAssign Driver not found"}, status=status.HTTP_404_NOT_FOUND) 
    
    
    
class FuelstationView(APIView):
    def post(self, request, *args, **kwargs):
        place_name = request.data.get('place_name')

        if not place_name:
            return Response({'error': 'Place name is required'}, status=status.HTTP_400_BAD_REQUEST)

        coordinates = get_coordinates(place_name)

        if not coordinates:
            return Response({'error': 'Failed to obtain coordinates'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lat, lng = coordinates
        
        fuel_station = get_fuel_stations(lat, lng)

        if not fuel_station:
            return Response({'error': 'Failed to obtain Fuel stations'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'fuel_station': fuel_station})

        
class WorkshopView(APIView):
    def post(self, request, *args, **kwargs):
        place_name = request.data.get('place_name')

        if not place_name:
            return Response({'error': 'Place name is required'}, status=status.HTTP_400_BAD_REQUEST)

        coordinates = get_coordinates(place_name)

        if not coordinates:
            return Response({'error': 'Failed to obtain coordinates'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lat, lng = coordinates
        
        workshop = get_workshops(lat, lng)

        if not workshop:
            return Response({'error': 'Failed to obtain Workshops'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'workshop': workshop})



