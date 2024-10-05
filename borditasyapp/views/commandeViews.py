from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from borditasyapp.models import Commande, Facture, Produit
from borditasyapp.serializers import CommandeFormSerializer, FactureSerializer, ProduitSerializer, CommandeListSerializer

@api_view(['POST'])
def create_commande(request):
        facture_data = request.data.get('facture')
        if facture_data:
            facture_serializer = FactureSerializer(data=facture_data)
            if facture_serializer.is_valid():
                saved_facture = facture_serializer.save()
                facture_id = saved_facture.id
                commandes_data = request.data.get('commandes', [])
                for commande_data in commandes_data:
                    commande_data["facture"]=facture_id
                    commande_serializer = CommandeFormSerializer(data=commande_data)
                    if commande_serializer.is_valid():
                        commande_serializer.save()
                    else:
                        return Response(commande_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(facture_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(facture_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_facture_with_commandes(request, id):
    try:
        facture = Facture.objects.get(id=id)
    except Facture.DoesNotExist:
        return Response({'error': 'Facture not found'}, status=status.HTTP_404_NOT_FOUND)

    facture_serializer = FactureSerializer(facture)
    commandes = Commande.objects.filter(facture=facture)
    commandes_serializer = CommandeListSerializer(commandes, many=True)

    response_data = {
        'facture': facture_serializer.data,
        'commandes': commandes_serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)

