from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
User = get_user_model()
from rest_framework.parsers import MultiPartParser, FormParser
class LoginView(TokenObtainPairView):
    """
    Custom login view that supports authentication via email or username.
    """

    def post(self, request, *args, **kwargs):
        identifier = request.data.get("username")  # could be username or email
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"message": "Username / Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # If identifier looks like an email
            if "@" in identifier:
                user = User.objects.get(email__iexact=identifier)
            else:
                user = User.objects.get(username__iexact=identifier)

            # Now authenticate using email (your USERNAME_FIELD)
            user = authenticate(email=user.email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)
                response =Response({
                    'message': 'Login successful',
                    'data': user_serializer.data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)
                return response

        except User.DoesNotExist:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class CreateUserView(APIView):
    """
    View for user registration.
    """
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class UserLogoutView(APIView):
    """
    View to log out the user and blacklist the refresh token.
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
            except Exception:
                return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        # Remove tokens from cookies
        response = Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class UpdateProfileView(UpdateAPIView):
    
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def get_object(self):
        return self.request.user
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not user.check_password(current_password):
            return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password or len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
