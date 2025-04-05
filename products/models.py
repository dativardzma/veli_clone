from django.db import models

# Create your models here.
class Characteristic(models.Model):
    brend = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    power = models.CharField(max_length=100)
    cable_length = models.FloatField(max_length=40)
    Warranty_period = models.IntegerField()

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(max_length=100)
    percent = models.IntegerField(default=0)
    characteristic = models.ManyToManyField(Characteristic)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")