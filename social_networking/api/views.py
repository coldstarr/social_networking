from rest_framework import throttling
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from .models import FriendRequest
from django.views.decorators.csrf import csrf_exempt
from .serializers import SendFriendRequestsSerializer, AcceptFriendRequestsSerializer, RejectFriendRequestsSerializer, ListFriendRequestsSerializer
from rest_framework.throttling import UserRateThrottle
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.serializers import ValidationError

@method_decorator(csrf_exempt, name='dispatch')
class SendFriendRequestAPIView(CreateAPIView):
    serializer_class = SendFriendRequestsSerializer
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        to_user_email = serializer.validated_data.get('to_user_email', None)

        if not to_user_email:
            raise ValidationError({'message': 'Missing to_user_email parameter.'})

        try:
            to_user = get_user_model().objects.get(email=to_user_email)
            from_user = self.request.user

            # Check if the friend request already exists
            existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()

            if existing_request:
                raise ValidationError({'message': 'Friend request already sent.'})
            
            # Check if trying to add friend request to oneself
            if from_user == to_user:
                raise ValidationError({'message': 'Cannot add friend request to oneself.'})

            # Create the friend request
            FriendRequest.objects.create(from_user=from_user, to_user=to_user)
            serializer.save()
            return Response({'message': 'Friend request sent successfully.'})

        except get_user_model().DoesNotExist:
            raise ValidationError({'message': 'User with this email does not exist.'})
        

        
class AcceptFriendRequestAPIView(UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = AcceptFriendRequestsSerializer

    def get_object(self):
        # Retrieve the friend request based on users and status
        to_user = self.request.user
        from_user_email = self.request.data.get('from_user_email')
        from_user = get_user_model().objects.get(email=from_user_email)
     
        return self.queryset.filter(
            from_user=to_user,
            to_user=from_user    
        ).first()

    def perform_update(self, serializer):
        if serializer.instance:
            # Create a reciprocal friend request for the other user
            from_user = serializer.instance.from_user
            to_user = serializer.instance.to_user

            # Check if the friend request already exists
            if serializer.instance=='pending':
                serializer.instance.status = 'accepted'
                serializer.save()
                FriendRequest.objects.create(from_user=to_user, to_user=from_user, status='accepted')
                return Response({'message': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)
            else:
                existing_request = FriendRequest.objects.filter(from_user=to_user, to_user=from_user).first()
                raise ValidationError({'message': f'Friend request is in {existing_request.status} state.'})
        else:
            raise ValidationError({'message': 'User with this email does not exist.'})


class RejectFriendRequestAPIView(UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = RejectFriendRequestsSerializer

    def get_object(self):
        # Retrieve the friend request based on users and status
        to_user = self.request.user
        from_user_email = self.request.data.get('from_user_email')
        from_user = get_user_model().objects.get(email=from_user_email)
     
        return self.queryset.filter(
            from_user=to_user,
            to_user=from_user    
        ).first()

    def perform_update(self, serializer):
        if serializer.instance:
            # Create a reciprocal friend request for the other user
            from_user = serializer.instance.from_user
            to_user = serializer.instance.to_user

            # Check if the friend request already exists
            if serializer.instance=='pending':
                serializer.instance.status = 'rejected'
                serializer.save()
                return Response({'message': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)
            else:
                existing_request = FriendRequest.objects.filter(from_user=to_user, to_user=from_user).first()
                raise ValidationError({'message': f'Friend request is in {existing_request.status} state.'})
        else:
            raise ValidationError({'message': 'User with this email does not exist.'})


class AcceptedFriendRequestAPIView(ListAPIView):
    serializer_class = ListFriendRequestsSerializer

    def get_queryset(self):
        # Otherwise, return only the accepted friend requests sent by the authenticated user
        return FriendRequest.objects.filter(from_user=self.request.user, status='accepted')

class PendingFriendRequestAPIView(ListAPIView):
    serializer_class = ListFriendRequestsSerializer

    def get_queryset(self):
        # Otherwise, return only the accepted friend requests sent by the authenticated user
        return FriendRequest.objects.filter(from_user=self.request.user, status='pending')