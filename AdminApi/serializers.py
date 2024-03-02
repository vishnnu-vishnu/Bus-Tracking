from rest_framework import serializers
from AdminApi.models import Admin,Route,Busstop,BusOwner,Passenger,Bus,RouteAssign



class AdminSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Admin
        fields=["id","username","password","email_address"]
   
    def create(self, validated_data):
        return Admin.objects.create_user(**validated_data)
    

class BusstopSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    routes=serializers.CharField(read_only=True)
    class Meta:
        model = Busstop
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Route
        fields = "__all__"


class BusownerviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=BusOwner
        fields=["id","username","proof","phone","name","address","is_approved"]


class PassengerviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Passenger
        fields=["id","name","phone","username","address","email_address"]


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