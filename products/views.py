from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product 
from .serializers import ProductSerializer
from rest_framework.generics import ListCreateAPIView

# Create your views here.
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
