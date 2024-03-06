from django.shortcuts import render
from rest_framework.views import APIView,status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import action


from Passesnger.serializers import PassengerSerializer,AssignedRoutesSerializer,RouteSerializer,BusstopSerializer,BusSerializer
from AdminApi.models import Passenger,Route,RouteAssign,Bus,Busstop



# Create your views here.


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
    
    
    @action(methods=['get'], detail=False)
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
            bus_data['route_assignments'] = [{'route_id': ra.route.id, 'start_time': ra.start_time, 'end_time': ra.end_time, 'route' : ra.route.name} for ra in route_assignments]

        response_data = {
            'status': 1,
            'buses': serializer.data
        }

        return Response(data={'status':1,'data':response_data}, status=status.HTTP_200_OK)