from rest_framework import serializers
from django.contrib.auth.models import User

from todo_app.models import Todo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )
        read_only_fields = (
            "id",
        )


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = (
            "id",
            "user",
            "complete",
            "description",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_user(self, obj):
        serializer = UserSerializer(obj.user)
        return serializer.data

    def create(self, validated_data):
        validated_data["user"] = self.initial_data["user"]
        return super().create(validated_data)
