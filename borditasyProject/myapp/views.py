from django.shortcuts import render
from rest_framework.views import APIView
from rest_framwork.response import Response
from rest_framework import status 
from .serializers import HelloSerializer

class HelloApiView(APIView):
    def get(self, request, format=None): 
        an_apiview = [
              'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
# Create your views here.
