from django.urls import path
from .views import (
    UserSignupAPIView, 
    UserLoginAPIView, 
    UserSearchAPIView, 
    SendFriendRequestAPIView, 
    ListFriendsAPIView, 
    ListPendingRequestsAPIView
)

urlpatterns = [
    path('signup/', UserSignupAPIView.as_view(), name='signup'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('search/', UserSearchAPIView.as_view(), name='user_search'),
    path('send-friend-request/', SendFriendRequestAPIView.as_view(), name='send_friend_request'),
    path('list-friends/', ListFriendsAPIView.as_view(), name='list_friends'),
    path('list-pending-requests/', ListPendingRequestsAPIView.as_view(), name='list_pending_requests'),
    
]
