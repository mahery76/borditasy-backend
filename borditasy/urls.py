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
<<<<<<< HEAD
from borditasyapp.views import HelloAPIView, create_produit, list_produits

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloAPIView.as_view(), name='hello'),
    path('api/produits/', create_produit, name='create_produit'),
    path('api/produits/list/', list_produits, name='list_produits')
]

=======
from borditasyapp.views import HelloAPIView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloAPIView.as_view(), name='hello')
]
>>>>>>> 58a0b4f8e34fd47538df1d89ddcb15800d230c6a