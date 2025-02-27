from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Order(models.Model):
    product = models.ManyToManyField(Product, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Add timestamp

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
