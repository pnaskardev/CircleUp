from rest_framework import serializers

from .models import FriendshipRequest, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'friends_count']
        # read_only_fields = ['id', 'created_at', 'created_by']


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ['id', 'created_for', 'created_by']
        # read_only_fields = ['id', 'created_at', 'created_by', 'status']
