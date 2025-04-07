from django.db import models

# Create your models here.
class Characteristic(models.Model):
    brend = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    power = models.CharField(max_length=100)
    cable_length = models.FloatField()

class Category(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    small_description = models.TextField(max_length=1000)
    price = models.FloatField()
    percent = models.IntegerField(default=0)
    discount_price = models.FloatField(editable=False, null=True, blank=True)
    characteristic = models.ManyToManyField(Characteristic)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    warranty_period = models.IntegerField(default=1, editable=False)

    def save(self, *args, **kwargs):
        if self.percent > 0:
            self.discount_price = self.price - (self.price * (self.percent / 100))
        else:
            self.discount_price = self.price
        
        if self.price > 1500:
            self.warranty_period = 2
        else:
            self.warranty_period = 1

        super().save(*args, **kwargs)

# ✅ New Model for Product Images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')
