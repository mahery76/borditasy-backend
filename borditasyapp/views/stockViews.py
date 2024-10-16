from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import connection

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


# @api_view(['GET'])
# def list_stock(request):
#     if request.method == 'GET':
#         stocks = Stock.objects.filter(prix_vente__isnull=False)
#         serializer = StockListSerializer(stocks, many=True)
#         return Response(serializer.data) 

    
@api_view(['GET'])
def list_stock(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT 
                    swr.produit_id as produit, 
                    swr.remaining_stock as quantite_stock,
                    pwap.prix_vente,
                    pwap.nom_produit,
                    pwap.prix_achat_dep
                FROM stock_with_remaining swr 
                JOIN ProductWithActualPrice pwap on swr.produit_id=pwap.id
                """)
            
            rows = cursor.fetchall()
            stocks = []

            for row in rows:
                stock = {
                    "quantite_stock": row[1],  # Accessing by index
                    "prix_vente": row[2],  # Accessing by index
                    "prix_achat_dep": row[4],  # Accessing by index
                    "produit": {
                        "id": row[0],  # Adjust this if you have more fields
                        "nom_produit": row[3],  # Adjust this if you have more fields
                        # Include other product fields here
                    }
                }
                stocks.append(stock)
        return Response(stocks)  # Changed from `stock` to `stocks`
            

# Now `stocks` contains all the data you can send in your response
        



