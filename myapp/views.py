from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from myapp.serializers import (
    UserSignupSerializer, 
    UserLoginSerializer, 
    FriendRequestSerializer
)
from myapp.models import CustomUser, Friendship, FriendRequest
from django.shortcuts import render, redirect
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from myapp.permissions import is_authenticated
from rest_framework.throttling import UserRateThrottle
from .throttles import FriendRequestThrottle


class UserSignupAPIView(APIView):
    def get(self, request):
        return render(request, 'accounts/signup.html')

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = CustomUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserSearchAPIView(APIView):
    def get(self, request):
        search_keyword = request.query_params.get('q', '')
        if search_keyword:
            users = CustomUser.objects.filter(
                Q(email__iexact=search_keyword) |
                Q(username__icontains=search_keyword)
            )

            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_users = paginator.paginate_queryset(users, request)
            return render(request, 'accounts/search_users.html', {'users': paginated_users})
        else:
            return render(request, 'accounts/search_users.html', {'message': 'Please provide a search keyword'})

# class SendFriendRequestAPIView(APIView):
#     throttle_classes = [FriendRequestThrottle]
#     def get(self, request):
#         return render(request, 'accounts/send_friend_request.html')

#     def post(self, request):
#         data = request.data
#         to_user_username = data.get('to_user_username')
#         to_user_email = data.get('to_user_email')
#         to_user = None
#         if to_user_username:
#             try:
#                 to_user = CustomUser.objects.get(username=to_user_username)
#             except CustomUser.DoesNotExist:
#                 return Response({'error': 'User with this username does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#         elif to_user_email:
#             try:
#                 to_user = CustomUser.objects.get(email=to_user_email)
#             except CustomUser.DoesNotExist:
#                 return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         if to_user:
#             # Check if a friend request already exists
#             existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists()
#             if existing_request:
#                 return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Create and save the friend request
#             serializer = FriendRequestSerializer(data={'from_user': request.user.id, 'to_user': to_user.id})
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'error': 'Recipient not found.'}, status=status.HTTP_404_NOT_FOUND)

class SendFriendRequestAPIView(APIView):
    throttle_classes = [FriendRequestThrottle]

    def get(self, request):
        return render(request, 'accounts/send_friend_request.html')

    def post(self, request):
        data = request.data

        # Get the ID of the user to send the friend request to
        to_user_id = data.get('to_user')
        if not to_user_id:
            return Response({'error': 'Please provide the ID of the user to send the friend request to.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists
        try:
            to_user = CustomUser.objects.get(id=to_user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with the provided ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if a friend request already exists
        existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists()
        if existing_request:
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the friend request
        serializer = FriendRequestSerializer(data={'from_user': request.user.id, 'to_user': to_user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListFriendsAPIView(APIView):
    def get(self, request):
        friends = Friendship.objects.all()
        return render(request, 'accounts/list_friends.html', {'friends': friends})


class ListPendingRequestsAPIView(APIView):
    def get(self, request):
        pending_requests = FriendRequest.objects.filter(accepted=False)
        return render(request, 'accounts/list_pending_requests.html', {'pending_requests': pending_requests})
