from rest_framework import serializers
from AdminApi.models import Passenger,Route,RouteAssign,Busstop,Bus

class PassengerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Passenger
        fields=["id","name","phone","username","address","password","email_address"]

    def create(self, validated_data):
        return Passenger.objects.create_user(**validated_data)


class RouteSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Route
        fields = "__all__"
        
class BusSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Bus
        fields = "__all__"
        

class AssignedRoutesSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = RouteAssign
        fields = "__all__"
        
        
class BusstopSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Busstop
        fields = "__all__"