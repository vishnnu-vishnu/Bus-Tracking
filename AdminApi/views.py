from django.shortcuts import render
from rest_framework.views import APIView,status
from AdminApi.serializers import AdminSerializer,RouteSerializer,BusstopSerializer,BusownerviewSerializer,PassengerviewSerializer,BusSerializer,AssignedRoutesSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from AdminApi.models import BusOwner,Route,Busstop,Admin,Passenger,Bus,RouteAssign
from rest_framework.decorators import action




class AdminCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Admin")
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)


class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = RouteSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = RouteSerializer(data=request.data)
        user_type = request.user.user_type
        if user_type == "Admin":
            if serializer.is_valid():
                serializer.save(is_active=True)
                return Response(data={'status':1,'data':serializer.data})
            else:
                error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
                return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Permission denied for others"}, status=status.HTTP_403_FORBIDDEN)
        
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
    
    
    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        route = Route.objects.get(id=id)
        route.is_active = False
        route.save()
        return Response(data={'status':1,"message": "route is now inactive"})
    


    @action(methods=["post"], detail=True)
    def add_stop(self, request, *args, **kwargs):
        serializer=BusstopSerializer(data=request.data)
        route_id=kwargs.get("pk")
        route_obj=Route.objects.get(id=route_id)
        if serializer.is_valid():
            serializer.save(routes=route_obj,is_active=True)
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)            


class OwnersView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated] 
     
    def list(self,request,*args,**kwargs):
        qs=BusOwner.objects.all()
        serializer=BusownerviewSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BusOwner.objects.get(id=id)
        serializer=BusownerviewSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    
    
    @action(detail=True, methods=["post"])
    def owner_approval(self, request, *args, **kwargs):
        owner_id = kwargs.get("pk")     
        owner_obj = BusOwner.objects.get(id=owner_id)
        owner_obj.is_approved = True
        owner_obj.save()
        serializer = BusownerviewSerializer(owner_obj)
        return Response(data={'status':1,'data':serializer.data})
    

class PassengerView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  
    def list(self,request,*args,**kwargs):
        qs=Passenger.objects.all()
        serializer=PassengerviewSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Passenger.objects.get(id=id)
        serializer=PassengerviewSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})
    

class BusView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  
    
    def list(self,request,*args,**kwargs):
        qs=Bus.objects.all()
        serializer=BusSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Bus.objects.get(id=id)
        serializer=BusSerializer(qs)
        return Response(data={'status':1,'data':serializer.data})            
    

class AssignedRoutesView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  
    
    def list(self,request,*args,**kwargs):
        qs=RouteAssign.objects.all()
        serializer=AssignedRoutesSerializer(qs,many=True)
        return Response(data={'status':1,'data':serializer.data})
    
    def retrieve(self, request, *args, **kwargs):
        try:
            assignment = RouteAssign.objects.get(pk=kwargs.get("pk"))
        except RouteAssign.DoesNotExist:
            return Response(
                {"error": "Assignment does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AssignedRoutesSerializer(assignment)
        response_data = serializer.data
        response_data['busowner'] = {
            'id': assignment.busowner.id,
            'name': assignment.busowner.name,
            'phone': assignment.busowner.phone,
            
        }
        response_data['bus'] = {
            'id': assignment.bus.id,
            'name': assignment.bus.name,
        }
        response_data['route'] = {
            'id': assignment.route.id,
            'name': assignment.route.name,
            'starts_from': assignment.route.starts_from,
            'ends_at': assignment.route.ends_at,
        }

        return Response(data={'status':1,'data':response_data})