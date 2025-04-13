from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    small_description = models.TextField(max_length=1000)
    price = models.FloatField()
    percent = models.IntegerField(default=0)
    discount_price = models.FloatField(editable=False, null=True, blank=True)
    characteristic = models.JSONField(default=dict)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    warranty_period = models.IntegerField(default=1, editable=False)
    monthly_payment = models.CharField(max_length = 50, editable=False)

    def save(self, *args, **kwargs):
        if self.percent > 0:
            self.discount_price = self.price - (self.price * (self.percent / 100))
        else:
            self.discount_price = self.price
        
        if self.price > 1500:
            self.warranty_period = 2
        else:
            self.warranty_period = 1

        if self.percent > 0:
            self.monthly_payment = self.discount_price / 12
        else:
            self.monthly_payment = self.price / 12

        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')

class CustomUser(AbstractUser):
    phone_number = models.IntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'acsses': str(refresh.access_token)}

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('user', 'product')

    def __str__(self):
        return f"Favorite: {self.user.username} - {self.product.name}"

class Basket(models.Model):
    ...