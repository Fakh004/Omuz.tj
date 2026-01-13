from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer
from .models import *


class RegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def login_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password') 
    if not username or not password:
        return Response(
            {'error':"please full all fields"},
            status=status.HTTP_400_BAD_REQUEST
        )
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({'success':'user logged in'}, status=status.HTTP_200_OK)
    return Response(
        {'error':"error with login"},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def logout_api_view(request):
    logout(request)
    return Response({'success':'user logged out'}, status=status.HTTP_200_OK)
    