"""
URL configuration for mountpass project.

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
from django.urls import path, include
from rest_framework import routers
from passapp import views
from .yasg import urlpatterns as doc_urls


router = routers.DefaultRouter()
router.register(r'Pereval', views.PerevalViewset, basename='pereval')
router.register(r'User', views.UserViewset, basename='user')
router.register(r'Coords', views.CoordsViewset, basename='coords')
router.register(r'Level', views.LevelViewset, basename='level')
router.register(r'Image', views.ImageViewset, basename='image')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

]

urlpatterns += doc_urls
