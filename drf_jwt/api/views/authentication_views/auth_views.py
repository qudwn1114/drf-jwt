# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from api.serializers.auth_serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer, RefreshTokenSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer    

class MyTokenRefreshView(TokenRefreshView):
    serializer_class=MyTokenRefreshSerializer

class TokenLogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)     
        if user is None: # 해당 user가 존재하지 않는 경우
            return Response(
                {"message": "존재하지않는 회원입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        token = MyTokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        outstandingToken = OutstandingToken.objects.get(token=refresh_token)
        response = Response(
            {
                "user": UserSerializer(user).data,
                "message": "login success",
                "jwt_token": {
                    "access_token": access_token,
                    "refresh_token_index_id": outstandingToken.id,
                    "refresh_token_exp" : outstandingToken.expires_at.timestamp()
                },
            },
            status=status.HTTP_200_OK
        )
        return response

class ReissueTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        refresh_token_index_id = request.data['refresh_token_index_id']
        try:
            refresh = OutstandingToken.objects.get(pk=refresh_token_index_id)
        except:
            return Response(
                {"message": "refresh token does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = MyTokenRefreshSerializer(data={'refresh':refresh.token})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        refresh_token = data['refresh']
        access_token = data['access']
        outstandingToken = OutstandingToken.objects.get(token=refresh_token)
        response = Response(
            {
                "user": UserSerializer(refresh.user).data,
                "message": "refresh token reissue",
                "jwt_token": {
                    "access_token": access_token,
                    "refresh_token_index_id": outstandingToken.id,
                    "refresh_token_exp" : outstandingToken.expires_at.timestamp()
                },
            },
            status=status.HTTP_200_OK
        )
        return response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        refresh_token_index_id = request.data['refresh_token_index_id']
        
        try:
            refresh = OutstandingToken.objects.get(pk=refresh_token_index_id)
        except:
            return Response(
                {"message": "refresh token does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RefreshTokenSerializer(data={'refresh':refresh.token})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)