from rest_framework import serializers
from .models import Produit, Stock, Commande, Facture

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all(), required=False)

    class Meta:
        model = Stock
        fields = '__all__'


class StockListSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(allow_null=True)

    class Meta:
        model = Stock
        fields = '__all__'


class CommandeFormSerializer(serializers.ModelSerializer):
    facture = serializers.PrimaryKeyRelatedField(queryset=Facture.objects.all(),required=False)
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all(),required=False)
    class Meta:
        model = Commande
        fields = '__all__'

class FactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facture
        fields = '__all__'

class CommandeListSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer()
    class Meta:
        model = Commande
        fields = ["id","produit","qte_produit"]

