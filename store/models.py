from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    product_slug = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='photos/products/')
    product_stock = models.IntegerField()
    product_available = models.BooleanField(default=True)
    product_category = models.ForeignKey("category.Category", verbose_name=("Category"), on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_detail", args=[self.product_category.slug, self.product_slug])

    def __str__(self):
        return self.product_name