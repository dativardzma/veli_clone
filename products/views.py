from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, generics
from .models import Product, Favorite, CustomUser, Category, Basket
from .serializers import ProductSerializer, FavoriteSerializer, UserSerializer, CategorySerializer, BasketSerializer, LoginSerializer, MyTokenObtainPairSerializer
from rest_framework.generics import ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView



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
            else:
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
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     refresh = user.tokens()
    #     result = {
    #         "username": serializer.data['username'],
    #         "email": serializer.data['email'],
    #         "phone_number": serializer.data['phone_number'],
    #         "password": serializer.validated_data['password'],
    #         "refresh": refresh['refresh'], 
    #         "access": refresh['acsses']
    #     }
    #     return Response(result, status=status.HTTP_201_CREATED)

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

class BasketViewSet(ModelViewSet):
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of basket products (Authentication Required)",
        security=[{'BearerAuth': []}],
        responses={200: BasketSerializer(many=True)}
    )
    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        baskets = self.get_queryset()
        data = []

        for basket in baskets:
            products_data = []
            for product in basket.products.all():
                product_data = {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "small_description": product.small_description,
                    "price": product.price,
                    "percent": product.percent,
                    "discount_price": product.discount_price,
                    "characteristic": product.characteristic,
                    "category": {
                        "id": product.category.id,
                        "name": product.category.name
                    },
                    "date_added": product.date_added,
                    "warranty_period": product.warranty_period,
                    "images": [
                        request.build_absolute_uri(img.image.url)
                        for img in product.images.all()
                    ]
                }
                products_data.append(product_data)

            data.append({
                "id": basket.id,
                "user": {
                    "id": basket.user.id,
                    "username": basket.user.username,
                    "email": basket.user.email,
                    "phone_number": basket.user.phone_number
                },
                "products": products_data
            })

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Add a product to basket",
        request_body=BasketSerializer, 
        security=[{'BearerAuth': []}],
        responses={201: BasketSerializer}
    )
    def post(self, request):
        serializer = BasketSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
        
class LoginViewSet(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login to get accses token",
        request_body = LoginSerializer,
        responses={200: ProductSerializer(many=True)}
    )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = user.tokens()
        return Response(
        {
            'username': user.username,
            'refresh': refresh['refresh'],
            'acsses': refresh['acsses']
        }
        )

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user  # Get the user from the token (authenticated user)
        # serializer = UserSerializer(user, context={'include_password': False})
        serializer = UserSerializer(user)  # Serialize user data
        return Response(serializer.data, status=status.HTTP_200_OK) 