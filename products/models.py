from django.db import models

# Create your models here.
class Characteristic(models.Model):
    brend = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    power = models.CharField(max_length=100)
    cable_length = models.FloatField()
    warranty_period = models.IntegerField()

class Category(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    percent = models.IntegerField(default=0)
    characteristic = models.ManyToManyField(Characteristic)
    image = models.ImageField(upload_to='product_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)