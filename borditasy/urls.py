"""
URL configuration for borditasy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from borditasyapp.views import HelloAPIView, create_produit, list_produits
from borditasyapp.views.produitViews import create_produit, list_produits,list_produits_with_price
from borditasyapp.views.stockViews import create_stock, list_stock
from borditasyapp.views.depenseViews import create_depense, list_depense
from borditasyapp.views.commandeViews import create_commande, list_facture_with_commandes
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/produits/', create_produit, name='create_produit'),
    path('api/produits/list/', list_produits, name='list_produits'),
    path('api/produits/list_price/', list_produits_with_price, name='list_produits_with_price'),
    path('api/stocks/', create_stock, name='create_stock'),
    path('api/stocks/list/', list_stock, name='list_stocks'),
    path('api/depenses/', create_depense, name='create_depense'),
    path('api/depenses/list', list_depense, name='list_depenses'),
    path('api/commandes/', create_commande, name='create_commande'),
    path('api/factures/<int:id>', list_facture_with_commandes, name='liste_facture'),
]




