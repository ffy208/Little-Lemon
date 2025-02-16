from django.test import TestCase
from restaurant.models import Menu
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.serializers import MenuSerializer

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item1 = Menu.objects.create(title="Pizza", price=120, inventory=50)
        self.item2 = Menu.objects.create(title="Pasta", price=90, inventory=40)

    def test_getall(self):
        response = self.client.get(reverse("menu-list"))  # 确保这个 URL 名称与你的 Django 路由一致
        menu_items = Menu.objects.all()
        serializer = MenuSerializer(menu_items, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
