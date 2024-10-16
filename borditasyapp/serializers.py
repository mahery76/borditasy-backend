from rest_framework import serializers
from .models import Produit, Stock, Commande, Facture, User

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all(), required=False)

    class Meta:
        model = Stock
        fields = '__all__'


class StockListSerializer(serializers.Serializer):
    produit = ProduitSerializer(allow_null=True)
    quantite_stock = serializers.IntegerField()
    prix_vente = serializers.IntegerField()

    # class Meta:
    #     model = Stock
    #     fields = ['quantite_stock', 'prix_vente', 'produit']

class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['designation_depense', 'quantite_stock', 'prix_achat_dep']
    
class DepenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['designation_depense', 'quantite_stock', 'prix_achat_dep']


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


class GetUserTokenSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'bio']


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # We don't want to return passwords in the response
    is_superuser = serializers.BooleanField(default=False)
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)  # Allow bio to be optional

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'bio']

class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'bio']

