from rest_framework import serializers
from AdminApi.models import BusOwner,Busstop,Route

class OwnerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=BusOwner
        fields=["id","username","password","phone","name","address"]
   
    def create(self, validated_data):
        return BusOwner.objects.create_user(**validated_data)
    