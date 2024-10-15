from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from borditasyapp.models import User

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password
from borditasyapp.serializers import CreateUserSerializer, GetUserTokenSerializer, GetAllUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserTokenSerializer
    permission_classes = [IsAuthenticated]


class UserLogIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, 
                                           context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"message": str(e.detail)}, status=400)


        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )

        if user is None:
            return Response({"message": "Invalid username or password"}, status=401)

        login(request, user)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_superuser': user.is_superuser,
            'bio': user.bio
        }, status=status.HTTP_200_OK)


class VerifyTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # If the user is authenticated, the token is valid
        return Response({'valid': True, 'user_id': request.user.id, 'username': request.user.username})


class CreateUserView(APIView):
    permission_classes = [AllowAny]  # No authentication needed to create a new user
    parser_classes = (MultiPartParser, FormParser)  # To handle form-data

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        
                                
        # Validate the data
        if serializer.is_valid():
            # If `is_superuser` is being requested, ensure the current user is an admin
            is_superuser = serializer.validated_data.get('is_superuser', False)
            # if is_superuser and not request.user.is_superuser:
            #         return Response({"message": "Only superusers can create other superusers."}, 
            #                         status=status.HTTP_403_FORBIDDEN)
            user = User.objects.create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email'),
                password=make_password(serializer.validated_data['password']),
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
                is_superuser=is_superuser,  # Set the superuser status
                is_staff=is_superuser,       # Set staff status if superuser
                bio=serializer.validated_data.get('bio', None)
            )
            # Optionally return token or user info
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_superuser': user.is_superuser,
                'bio': user.bio
            }, status=status.HTTP_201_CREATED)
        
            # If invalid data, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetAllUsers(APIView):
    permission_classes = [AllowAny]  # No authentication needed to create a new user
    def get(self, request):
        serializer = GetAllUserSerializer(data=request.data)
        users = User.objects.all()
        serializer = GetAllUserSerializer(users, many=True)
        return Response(serializer.data) 