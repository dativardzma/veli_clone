from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Product, Favorite
from .serializers import ProductSerializer, FavoriteSerializer
from rest_framework.generics import ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

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


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        session_id = self.request.query_params.get('session_id')
        if session_id:
            return Favorite.objects.filter(session_id=session_id)
        return Favorite.objects.none()

    def create(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        product_id = request.data.get('product')

        if not session_id or not product_id:
            return Response({'error': 'session_id and product are required'}, status=status.HTTP_400_BAD_REQUEST)

        favorite, created = Favorite.objects.get_or_create(session_id=session_id, product_id=product_id)

        if not created:
            return Response({'message': 'Already in favorites'}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        print(Favorite.objects.all())
        favorite_id = kwargs.get('pk')

        try:
            instance = Favorite.objects.get(id=favorite_id)  # Fetch the object
        except Favorite.DoesNotExist:
            return Response({"detail": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)
        return Response({"message": "Favorite deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
