from rest_framework import serializers
from .models import FriendRequest
from users.serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import get_user_model

class SendFriendRequestsSerializer(serializers.ModelSerializer):
    to_user_email = serializers.EmailField(write_only=True)

    class Meta:
        model = FriendRequest
        fields = ['to_user_email']

class AcceptFriendRequestsSerializer(serializers.ModelSerializer):
    from_user_email = serializers.EmailField(write_only=True)

    class Meta:
        model = FriendRequest
        fields = ['from_user_email']

class RejectFriendRequestsSerializer(serializers.ModelSerializer):
    from_user_email = serializers.EmailField(write_only=True)

    class Meta:
        model = FriendRequest
        fields = ['from_user_email']

class ListFriendRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['from_user', 'to_user', 'status', 'created_at']