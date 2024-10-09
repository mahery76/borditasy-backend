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
    prix_achat_dep = models.FloatField(null=False)
    prix_vente = models.FloatField(null=True, blank=True)  
    produit = models.ForeignKey(Produit, on_delete=models.DO_NOTHING, null=True, blank=True)  
    date_stock= models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.designation_depense

class Facture(models.Model):
    est_payee = models.BooleanField()
    date_facture = models.DateTimeField(default=timezone.now)
    

class Commande(models.Model):
    qte_produit = models.FloatField()
    facture = models.ForeignKey(Facture, on_delete=models.DO_NOTHING)
    produit = models.ForeignKey(Produit, on_delete=models.DO_NOTHING)


        
