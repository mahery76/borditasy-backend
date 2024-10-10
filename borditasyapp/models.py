from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

class Produit(models.Model):
    nom_produit = models.CharField(max_length=255)
    quantite_minimum = models.PositiveIntegerField(default=0)


class Stock(models.Model):
    designation_depense = models.CharField(max_length=255, null=True, blank=True)
    quantite_stock = models.FloatField(null=True, blank=True)
    prix_achat_dep = models.FloatField()
    prix_vente = models.FloatField(null=True, blank=True)  
    produit = models.ForeignKey(Produit, on_delete=models.DO_NOTHING, null=True, blank=True)  
    date_stock= models.DateField(auto_now=True)


class Facture(models.Model):
    est_payee = models.BooleanField()
    date_facture = models.DateTimeField(default=timezone.now)
    

class Commande(models.Model):
    qte_produit = models.FloatField()
    facture = models.ForeignKey(Facture, on_delete=models.DO_NOTHING)
    produit = models.ForeignKey(Produit, on_delete=models.DO_NOTHING)

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True)

    # def __str__(self):
    #     return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
    
        # .object not found fixed when adding 'rest_framework.authtoken' to installed app
        Token.objects.create(user=instance)

        # integrity erro when deleting a user from django admin