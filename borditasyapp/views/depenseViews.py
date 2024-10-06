from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from borditasyapp.models import Stock
from borditasyapp.serializers import DepenseSerializer, DepenseListSerializer

@api_view(['POST'])
def create_depense(request):
    if request.method == 'POST':
        serializer = DepenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_depense(request):
    if request.method == 'GET':
        stocks = Stock.objects.filter(prix_vente__isnull=True)
        serializer = DepenseListSerializer(stocks, many=True)
        return Response(serializer.data) 



