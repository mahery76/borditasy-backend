from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from borditasyapp.models import User
from borditasyapp.serializers import GetUserTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserTokenSerializer
    permission_classes = [IsAuthenticated]


class UserLogIn(ObtainAuthToken):
    def getUserTokens(self, request, *args, **kwargs):
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

        token = Token.objects.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'id': user.id,
            'username': user.username
        })


class VerifyTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # If the user is authenticated, the token is valid
        return Response({'valid': True, 'user_id': request.user.id, 'username': request.user.username})
