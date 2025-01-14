from rest_framework.throttling import UserRateThrottle

class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend_request'
    rate = '3/minute'
