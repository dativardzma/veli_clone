from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework.generics import ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductFilter(ModelViewSet):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of products",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category", type=openapi.TYPE_STRING),
            openapi.Parameter('filter', openapi.IN_QUERY, description="Sort by date, price, etc.", type=openapi.TYPE_STRING)
        ],
        responses={200: ProductSerializer(many=True)}
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        filt = self.request.query_params.get('filter', None)

        queryset = Product.objects.all() 

        if category:
            if category.isdigit():
                queryset = queryset.filter(category__id=int(category))
            else:
                queryset = queryset.filter(category__name__iexact=category) 

        if filt == "date":
            queryset = queryset.order_by('-date_added')
        elif filt == "discount":
            queryset = queryset.order_by('-percent')
        elif filt == "Price_Descending":
            queryset = queryset.order_by('-price')
        elif filt == "Price_Ascending":
            queryset = queryset.order_by('price')

        return queryset
