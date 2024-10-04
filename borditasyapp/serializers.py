from rest_framework import serializers
from .models import Produit, Stock

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

class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['designation_depense', 'quantite_stock', 'prix_achat_dep']
    
class DepenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['designation_depense', 'quantite_stock', 'prix_achat_dep']







