from rest_framework import serializers
from .models import Event, User  # Assuming User is the model for the owner

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class EventSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    attendees = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "location",
            "owner",
            "attendees",
            "created_at",
        ]
        read_only_fields = ["attendees", "created_at", "owner"]

    def create(self, validated_data):
        user = self.context.get("request").user  
        validated_data["owner"] = user  
        event = Event.objects.create(**validated_data)
        return event

    def update(self, instance, validated_data):
        validated_data.pop("owner", None)
        return super().update(instance, validated_data)
