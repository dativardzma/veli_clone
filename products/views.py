from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, generics
from .models import Product, Favorite, CustomUser, Category
from .serializers import ProductSerializer, FavoriteSerializer, UserSerializer, CategorySerializer
from rest_framework.generics import ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.forms.models import model_to_dict


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ProductFilter(ModelViewSet):
    queryset = Product.objects.all()
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
                queryset = queryset.filter(category__name__iexact=category)
        print(queryset)

        if filt == "date":
            queryset = queryset.order_by('-date_added')
        elif filt == "discount":
            queryset = queryset.order_by('-percent')
        elif filt == "Price_Descending":
            queryset = queryset.order_by('-price')
        elif filt == "Price_Ascending":
            queryset = queryset.order_by('price')

        return queryset

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = user.tokens()
        result = {
            "username": serializer.data['username'],
            "email": serializer.data['email'],
            "phone_number": serializer.data['phone_number'],
            "password": serializer.data['password'],
            "refresh": refresh['refresh'], 
            "access": refresh['acsses']
        }
        return Response(result, status=status.HTTP_201_CREATED)

class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of favorite products (Authentication Required)",
        security=[{'BearerAuth': []}],
        responses={200: FavoriteSerializer(many=True)}
    )
    def list(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Add a product to favorites",
        request_body=FavoriteSerializer, 
        security=[{'BearerAuth': []}],
        responses={201: FavoriteSerializer}
    )
    def create(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)