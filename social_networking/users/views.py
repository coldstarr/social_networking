from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from rest_framework.filters import SearchFilter
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator

@authentication_classes([])  
@permission_classes([AllowAny])
class Home(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


@authentication_classes([])  
@permission_classes([AllowAny])
@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@authentication_classes([])  
@permission_classes([AllowAny])
@method_decorator(csrf_exempt, name='dispatch')
class SignupAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # If the user was successfully created, log them in
        if response.status_code == status.HTTP_201_CREATED:
            user = get_user_model().objects.get(email=request.data.get('email').lower())
            login(request, user)
        
        return response
    
    def perform_create(self, serializer):
        user = serializer.save()
        return user
    
# Create your views here.
class UserSearchAPIView(ListAPIView):
    queryset =  CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['=email', '$name']