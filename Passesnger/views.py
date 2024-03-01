from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from Passesnger.serializers import PassengerSerializer



# Create your views here.


class PassengerCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=PassengerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Passenger")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
