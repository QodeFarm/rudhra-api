from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

#add your urls

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'products', ProductsViewSet)
router.register(r'sendmail', SendmailViewSet, basename='sendmail')

urlpatterns = [
    path('',include(router.urls)),
]