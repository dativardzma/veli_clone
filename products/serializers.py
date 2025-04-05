from rest_framework import serializers
from .models import Characteristic, Product, ProductImage

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicSerializer(many=True)
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Product
        fields = ['name', 'price', 'percent', 'characteristic', 'images']

    def create(self, validated_data):
        images = validated_data.pop("images")
        product = Product.objects.create(name=validated_data["name"])
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]

