from django.contrib import admin
from .models import Produit
from .models import Stock
from .models import Facture
from .models import Commande
from .models import User

admin.site.register(Produit)
admin.site.register(Stock)
admin.site.register(Facture)
admin.site.register(Commande)
admin.site.register(User)
