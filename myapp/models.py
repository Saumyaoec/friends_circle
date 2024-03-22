from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

class Friendship(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendships1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendships2')
    created_at = models.DateTimeField(auto_now_add=True)