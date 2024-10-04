from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from borditasyapp.models import Stock
from borditasyapp.serializers import StockSerializer, StockListSerializer

@api_view(['POST'])
def create_stock(request):
    if request.method == 'POST':
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_stock(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        serializer = StockListSerializer(stocks, many=True)
        return Response(serializer.data) 



