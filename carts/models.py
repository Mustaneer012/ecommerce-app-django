from django.db import models
from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=20, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)  # Assuming Variation is defined in store.models
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.product_price * self.quantity
    
    def __unicode__(self):
        return self.product