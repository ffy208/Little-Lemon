
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    guest_number = models.IntegerField()
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Add code to create Menu model

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(max_length=1000,
                                   default="")  # New description field
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # 关联分类
    is_item_of_the_day = models.BooleanField(default=False)  # 新增字段

    def __str__(self):
        return self.name






# ✅ 购物车模型 (Cart)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 购物车属于某个用户
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)  # 购物车关联的菜单项
    quantity = models.IntegerField(default=1)  # 数量

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name} ({self.quantity})"

# ✅ 订单模型 (Order)
class Order(models.Model):
    STATUS_CHOICES = [
        (0, 'Out for delivery'),
        (1, 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 下单的用户
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="deliveries"
    )  # 分配的送货员 (可选)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)  # 订单状态
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {dict(self.STATUS_CHOICES)[self.status]}"

# ✅ 订单详情模型 (OrderItem)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")  # 订单
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)  # 关联的菜单项
    quantity = models.IntegerField(default=1)  # 数量

    def __str__(self):
        return f"Order {self.order.id} - {self.menu_item.name} ({self.quantity})"

