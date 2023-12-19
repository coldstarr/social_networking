from django.urls import path
from .views import SendFriendRequestAPIView, AcceptedFriendRequestAPIView, RejectFriendRequestAPIView, AcceptFriendRequestAPIView, PendingFriendRequestAPIView

urlpatterns = [
    path('send/', SendFriendRequestAPIView.as_view(), name='friend_request_send'),
    path('accept/', AcceptFriendRequestAPIView.as_view(), name='friend_request_accept'),
    path('reject/', RejectFriendRequestAPIView.as_view(), name='friend_request_reject'),
    path('accepted_friend_requests/', AcceptedFriendRequestAPIView.as_view(), name='list_accepted_friend_requests'),
    path('pending_friend_requests/', PendingFriendRequestAPIView.as_view(), name='list_pending_friend_requests')
]