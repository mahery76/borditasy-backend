from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

class HelloAPIView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, world!'})
