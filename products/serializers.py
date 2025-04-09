from rest_framework import serializers
from .models import Product, Category, ProductImage, Favorite

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

# class CharacteristicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Characteristic
#         fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    # characteristic = CharacteristicSerializer(many=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'percent', 'discount_price', 'characteristic', 'images', 'category', 'description', 'small_description', 'warranty_period']

class FavoriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Favorite
        fields = ['session_id', 'product', 'product_details']