from django.shortcuts import render
from rest_framework.views import APIView,status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import action
from Passesnger.serializers import PassengerSerializer,AssignedRoutesSerializer,RouteSerializer,BusstopSerializer,BusSerializer
from AdminApi.models import Passenger,Route,RouteAssign,Bus,Busstop
import nexmo
from django.http import HttpResponse

from Passesnger.services import get_coordinates,get_Bus_stations,get_workshops,get_fuel_stations






class PassengerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=PassengerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Passenger")
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)     
        
        
class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = RouteSerializer
        
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
        bus_serializer = AssignedRoutesSerializer(route.routeassign_set.all(), many=True)
        response_data = route_serializer.data
        response_data['bus assigned'] = bus_serializer.data
        response_data['stops'] = stops_serializer.data
        return Response(data={'status':1,'data':response_data})
    

    @action(methods=['post'], detail=False)
    def search_route(self, request):
        starts_from = request.data.get('starts_from')
        ends_at = request.data.get('ends_at')

        if starts_from and ends_at:
            routes = Route.objects.filter(starts_from=starts_from, ends_at=ends_at)
        elif ends_at:
            routes = Route.objects.filter(ends_at=ends_at)
        elif starts_from:
            routes = Route.objects.filter(starts_from=starts_from)
        else:
            return Response({"status": 0, "error": "Please provide at least one place"}, status=status.HTTP_400_BAD_REQUEST)

        buses_on_routes = Bus.objects.filter(routeassign__route__in=routes)
        serializer = BusSerializer(buses_on_routes, many=True)
        
        for bus_data in serializer.data:
            bus_id = bus_data['id']
            route_assignments = RouteAssign.objects.filter(bus_id=bus_id)
            bus_data['route_assignments'] = [{'route_id': ra.route.id, 'start_time': ra.start_time, 'end_time': ra.end_time, 'route': ra.route.name} for ra in route_assignments]
            bus_data['route_ids'] = [ra.route.id for ra in route_assignments]  # Include route IDs within bus data

        return Response(data={'status': 1, 'buses': serializer.data}, status=status.HTTP_200_OK)

        
 

class AlertMessageView(APIView):
    def post(self, request):
        client = nexmo.Client(key='af5fc598', secret='VW4M2qLTBeb6Ejvu')

        response = client.send_message({
            'from': 'YourApp',
            'to': '+917994620947',  #update with your number
            'text': 'Iam in danger.Please help me out!',
        })

        if response['messages'][0]['status'] == '0':
            return HttpResponse('SOS message sent successfully!')
        else:
            return HttpResponse('Failed to send SOS message!')
        
        
class BusStationView(APIView):
    def post(self, request, *args, **kwargs):
        place_name = request.data.get('place_name')

        if not place_name:
            return Response({'error': 'Place name is required'}, status=status.HTTP_400_BAD_REQUEST)

        coordinates = get_coordinates(place_name)

        if not coordinates:
            return Response({'error': 'Failed to obtain coordinates'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lat, lng = coordinates
        
        bus_station = get_Bus_stations(lat, lng)

        if not  bus_station:
            return Response({'error': 'Failed to obtain Bus stations'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'bus_station':  bus_station})
    

    
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