from django.db import models
from django.utils import timezone

class Produit(models.Model):
    nom_produit = models.CharField(max_length=255)
    quantite_minimum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom_produit

class Stock(models.Model):
    designation_depense = models.CharField(max_length=255, null=True, blank=True)
    quantite_stock = models.FloatField(null=True, blank=True)
    prix_achat_dep = models.FloatField()
    prix_vente = models.FloatField(null=True, blank=True)  
    produit = models.ForeignKey(Produit, on_delete=models.DO_NOTHING, null=True, blank=True)  
    
    def __str__(self):
        return self.designation_depense

class PrixProduit(models.Model):
    prix_produit = models.FloatField()
    date_prix_produit = models.DateField()
    produit = models.ForeignKey(Produit, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.prix_produit
from django.utils import timezone

class Facture(models.Model):
    est_payee = models.BooleanField()
    date_facture = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.est_payee

class Commande(models.Model):
    qte_produit = models.FloatField()
    facture = models.ForeignKey(Facture, on_delete=models.DO_NOTHING)
    produit = models.ForeignKey(Produit, on_delete=models.DO_NOTHING)


        
