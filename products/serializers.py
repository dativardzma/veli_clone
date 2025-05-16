from rest_framework import serializers
from .models import Product, Category, ProductImage, Favorite, CustomUser, Basket
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims if you want (optional)
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user details to the response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'phone_number': self.user.phone_number,
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password will only be used for write operations (POST, PUT)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password']  # Include password in the fields

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        self._tokens = MyTokenObtainPairSerializer.get_token(user)
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Only add tokens if available
        if hasattr(self, '_tokens'):
            rep['refresh'] = str(self._tokens)
            rep['access'] = str(self._tokens.access_token)

        return rep


    def update(self, instance, validated_data):
        # Handle password update properly (hashing it before saving)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Ensure password is hashed
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

    # def __init__(self, *args, **kwargs):
    #     # Remove password field dynamically
    #     include_password = kwargs.get('context', {}).get('include_password', True)

    #     super().__init__(*args, **kwargs)

    #     if not include_password:
    #         self.fields.pop('password', None)  # Remove password field if not needed

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product']
        read_only_fields = ['user']

class BasketSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())

    class Meta:
        model = Basket
        fields = ['products']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the authenticated user from the request context
        products = validated_data.pop('products')  # Extract products

        # Either get existing basket or create a new one for this user
        basket, _ = Basket.objects.get_or_create(user=user)

        basket.products.set(products)  # Replace with provided products
        basket.save()
        return basket
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']