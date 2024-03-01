from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView,status
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response
from BusOwner.serializers import OwnerSerializer,BusstpSerializer,RouteSerializer
from AdminApi.models import Busstop,BusOwner,Route

# Create your views here.

class OwnerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Bus Owner")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


# class PlaceCreate(ViewSet):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]
#     serializer_class = PlaceSerializer
    
#     def create(self,request,*args,**kwargs):
#         serializer=PlaceSerializer(data=request.data)
#         owner_id=request.user.id
#         print(owner_id)
#         owner_object=BusOwner.objects.get(id=owner_id)
#         if owner_object:
#             if serializer.is_valid():
#                 serializer.save(owner=owner_object)
#                 return Response(data=serializer.data)
#             else:
#                 return Response(data=serializer.errors)
#         else:
#             return Response(request,"Owner not found")
        
#     def list(self,request,*args,**kwargs):
#         owner_id=request.user.id
#         owner_object=BusOwner.objects.get(id=owner_id)
#         qs=Place.objects.filter(owner=owner_object)
#         serializer=PlaceSerializer(qs,many=True)
#         return Response(data=serializer.data)
    
#     def retrieve(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         qs=Place.objects.get(id=id)
#         serializer=PlaceSerializer(qs)
#         return Response(data=serializer.data)
    
    
#     def destroy(self,request,*args,**kwargs):
#         id = kwargs.get("pk")
#         place = Place.objects.get(id=id)
#         place.is_active = False
#         place.save()
#         return Response(data={"message": "Place is now inactive"})
        

class RouteView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = RouteSerializer
    
    def create(self,request,*args,**kwargs):
        serializer=RouteSerializer(data=request.data)
        owner_id=request.user.id
        print(owner_id)
        owner_object=BusOwner.objects.get(id=owner_id)
        if owner_object:
            if serializer.is_valid():
                serializer.save(owners=owner_object)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(request,"Busowner not found")
        
    def list(self,request,*args,**kwargs):
        owner_id=request.user.id
        owner_object=BusOwner.objects.get(id=owner_id)
        qs=Route.objects.filter(owners=owner_object)
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
    
    # http://127.0.0.1:8000/vendor/foods/1
    # @action(methods=["post"],detail=True)
    # def add_food(self,request,*args,**kwargs):
    #     serializer=FoodSerializer(data=request.data)
    #     cat_id=kwargs.get("pk")
    #     category_obj=Category.objects.get(id=cat_id)
    #     vendor=request.user.id
    #     vendor_object=Vendor.objects.get(id=vendor) 
    #     if serializer.is_valid():
    #         serializer.save(category=category_obj,vendor=vendor_object,is_active=True)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
    

