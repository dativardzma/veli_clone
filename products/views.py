from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework.generics import ListCreateAPIView


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        filt = self.request.query_params.get('filter', None)

        if filt == "date":
            return Product.objects.all().order_by('-date_added')
        if filt == "discount":
            return Product.objects.all().order_by('-percent')
        if filt == "Price_Descending":
            return Product.objects.all().order_by('-price')
        if filt == "Price_Ascending":
            return Product.objects.all().order_by('price')
        
        return Product.objects.all()
