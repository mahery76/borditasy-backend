from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from borditasyapp.models import Produit
from borditasyapp.serializers import ProduitSerializer

@api_view(['POST'])
def create_produit(request):
    if request.method == 'POST':
        serializer = ProduitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_produits(request):
    if request.method == 'GET':
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data) 


@api_view(['GET'])
def list_produits_with_price(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ProductWithActualPrice")
            columns = [col[0] for col in cursor.description]
            produits_with_price = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return Response(produits_with_price, status=status.HTTP_200_OK)


