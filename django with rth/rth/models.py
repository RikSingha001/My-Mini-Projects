from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=10)
    total_price = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Delivered', 'Delivered')
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.meal_type}"
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def get_subtotal(self):
        return self.price * self.quantity
