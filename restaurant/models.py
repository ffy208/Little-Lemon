from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    guest_number = models.IntegerField(default=1)  # 默认至少 1 人
    comment = models.CharField(max_length=1000, blank=True, null=True)

    reservation_date = models.DateField(default=now)  # 设置默认值为当前日期
    reservation_slot = models.IntegerField(default=12)  # 默认时间为 12 点

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reservation_date} at {self.reservation_slot}"


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(max_length=1000, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_item_of_the_day = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} : {str(self.price)}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name} ({self.quantity})"


class Order(models.Model):
    STATUS_CHOICES = [
        (0, 'Out for delivery'),
        (1, 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="deliveries"
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {dict(self.STATUS_CHOICES)[self.status]}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Order {self.order.id} - {self.menu_item.name} ({self.quantity})"
