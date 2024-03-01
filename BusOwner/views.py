from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


from rest_framework.views import APIView,status
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response
from BusOwner.serializers import OwnerSerializer
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

        return Response(data=serializer.data)
    



    
    




