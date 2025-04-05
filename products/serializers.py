from rest_framework import serializers
from .models import Characteristic, Product, ProductImage

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]

class ProductSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicSerializer(many=True)
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'percent', 'characteristic', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        characteristics_data = validated_data.pop("characteristic", [])
        
        product = Product.objects.create(**validated_data)

        # Handle ManyToMany Characteristic
        for char_data in characteristics_data:
            char_instance, created = Characteristic.objects.get_or_create(**char_data)
            product.characteristic.add(char_instance)

        # Handle Image Uploads
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product