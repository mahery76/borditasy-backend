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



