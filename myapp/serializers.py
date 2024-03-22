from rest_framework import serializers
from .models import CustomUser, FriendRequest

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)


from rest_framework import serializers
from .models import FriendRequest, CustomUser

class FriendRequestSerializer(serializers.ModelSerializer):
    to_user_input = serializers.CharField()

    class Meta:
        model = FriendRequest
        fields = ['to_user_input']

    def validate(self, data):
        to_user_input = data.get('to_user_input')

        try:
            # Check if input is an email
            if '@' in to_user_input:
                user = CustomUser.objects.get(email=to_user_input)
            else:
                user = CustomUser.objects.get(username=to_user_input)

            data['to_user'] = user
            return data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
