from rest_framework import serializers
from AdminApi.models import Passenger

class PassengerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Passenger
        fields=["id","name","phone","username","address","password","email_address"]

    def create(self, validated_data):
        return Passenger.objects.create_user(**validated_data)


