from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

class AuthAPIView(APIView):
    def post(self, request):
        # step 0: Validation
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # step 1: Authentication
        username = serializer.validated_data['username']  # admin
        password = serializer.validated_data['password']  # 123
        user = authenticate(username=username, password=password)  # user / None

        # step 2: Token function
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        users = User.objects.create_user(username=username, password=password, is_active=False)
        # create code (6-symbol)
        return Response(data={'user_id': users.id}, status=status.HTTP_201_CREATED)

