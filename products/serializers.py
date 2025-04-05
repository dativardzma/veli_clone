from rest_framework import serializers
from .models import Characteristic, Product

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicSerializer(many=True)
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = Product
        fields = ['name', 'price', 'percent', 'characteristic', 'image_url']
