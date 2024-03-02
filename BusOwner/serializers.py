from rest_framework import serializers
from AdminApi.models import BusOwner,Busstop,Route,BusDriver,RouteAssign,Bus

class OwnerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    is_approved=serializers.CharField(read_only=True)

    class Meta:
        model=BusOwner
        fields=["id","username","password","phone","name","address","is_approved"]
   
    def create(self, validated_data):
        return BusOwner.objects.create_user(**validated_data)
 
 
class BusSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    busowner=serializers.CharField(read_only=True)
    class Meta:
        model = Bus
        fields = "__all__"

      
class BusDriverSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    busowner=serializers.CharField(read_only=True)
    class Meta:
        model = BusDriver
        fields = "__all__"  
        
        
class RouteSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Route
        fields = "__all__"
        
class BusstopSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model = Busstop
        fields = "__all__"
        
        

class RouteAssignSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    busowner=serializers.CharField(read_only=True)
    route=serializers.CharField(read_only=True)
    class Meta:
        model = RouteAssign
        fields = "__all__" 
        
        
class RouteAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAssign
        fields = "__all__" 
        