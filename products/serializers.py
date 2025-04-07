from rest_framework import serializers
from .models import Characteristic, Product, Category

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicSerializer(many=True)
    image_url = serializers.SerializerMethodField()
    category = CategorySerializer()

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Product
        fields = ['name', 'price', 'percent', 'discount_price', 'characteristic', 'image_url', 'category', 'description', 'small_description', 'warranty_period' ]
