from django.shortcuts import render
from rest_framework.views import APIView,status
from AdminApi.serializers import AdminSerializer,BusstpSerializer,RouteSerializer,BusownerviewSerializer,PassengerviewSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from AdminApi.models import BusOwner,Route,Busstop,Admin,Passenger
from rest_framework.decorators import action



# Create your views here.

class AdminCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Admin")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = RouteSerializer
    
    def create(self,request,*args,**kwargs):
        serializer=RouteSerializer(data=request.data)
        admin_id=request.user.id
        print(admin_id)
        admin_object=Admin.objects.get(id=admin_id)
        if admin_object.user_type=="Admin":
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(request,"Permission Denied For  Others")
        
    def list(self,request,*args,**kwargs):
        qs=Route.objects.all()
        serializer=RouteSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Route.objects.get(id=id)
        serializer=RouteSerializer(qs)
        return Response(data=serializer.data)
    
    
    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        route = Route.objects.get(id=id)
        route.is_active = False
        route.save()
        return Response(data={"message": "route is now inactive"})
    


    @action(methods=["post"], detail=True)
    def add_stop(self, request, *args, **kwargs):
        stop_data_list = request.data.get('stops', [])  
        route_id = kwargs.get("pk")
        route_obj = Route.objects.get(id=route_id)
        admin = request.user.id
        admin_object = Admin.objects.get(id=admin)

        errors = []
        successes = []
        if admin_object.user_type=="Admin":

            for stop_data in stop_data_list:
                serializer = BusstpSerializer(data=stop_data)
                if serializer.is_valid():
                    serializer.save(routes=route_obj, is_active=True)
                    successes.append(serializer.data)
                else:
                    errors.append(serializer.errors)

            if errors:
                return Response(data={"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"Stops Added Sucessfully": successes}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        


class OwnersView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  
    def list(self,request,*args,**kwargs):
        qs=BusOwner.objects.all()
        serializer=BusownerviewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=BusOwner.objects.get(id=id)
        serializer=BusownerviewSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(detail=True, methods=["post"])
    def owner_approval(self, request, *args, **kwargs):
        owner_id = kwargs.get("pk")
        owner_obj = BusOwner.objects.get(id=owner_id)
        owner_obj.is_approved = True
        owner_obj.save()
        serializer = BusownerviewSerializer(owner_obj)
        return Response(serializer.data)
    

class PassengerView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]  
    def list(self,request,*args,**kwargs):
        qs=Passenger.objects.all()
        serializer=PassengerviewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Passenger.objects.get(id=id)
        serializer=PassengerviewSerializer(qs)
        return Response(data=serializer.data)            
    

