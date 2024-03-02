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

# Create your views here.

class OwnerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Bus Owner")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class BusView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=BusSerializer(data=request.data)
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        if serializer.is_valid():
            serializer.save(busowner=busowner_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=Bus.objects.filter(busowner=busowner_obj)
        serializer=BusSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Bus.objects.get(id=id)
        serializer=BusSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Bus.objects.get(id=id)
            instance.delete()
            return Response({"msg": "bus removed"})
        except Bus.DoesNotExist:
            return Response({"msg": "bus not found"}, status=status.HTTP_404_NOT_FOUND)
  

class BusDriverView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        serializer=BusDriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(busowner=busowner_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=BusDriver.objects.filter(busowner=busowner_obj)
        serializer=BusDriverSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BusDriver.objects.get(id=id)
        serializer=BusDriverSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =BusDriver.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Bus Driver removed"})
        except BusDriver.DoesNotExist:
            return Response({"msg": "Bus Driver not found"}, status=status.HTTP_404_NOT_FOUND)    



class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
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
        response_data = route_serializer.data
        response_data['stops'] = stops_serializer.data
        return Response(response_data)
    

    @action(methods=["post"], detail=True)
    def route_assign(self, request, *args, **kwargs):
        serializer=RouteAssignSerializer(data=request.data)
        route_id=kwargs.get("pk")
        route_obj=Route.objects.get(id=route_id)
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        if serializer.is_valid():
            bus_id=request.data.get('bus')
            bus_obj=Bus.objects.get(id=bus_id)
            bus_obj.is_active=True
            bus_obj.save()
            serializer.save(route=route_obj,busowner=busowner_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)      
    

class RouteAssignsView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        busowner_id=request.user.id
        busowner_obj=BusOwner.objects.get(id=busowner_id)
        qs=RouteAssign.objects.filter(busowner=busowner_obj)
        serializer=RouteAssignedSerializer(qs,many=True)
        return Response(data=serializer.data)   
    
    
    




