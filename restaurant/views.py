from .forms import BookingForm
from django.shortcuts import render, get_object_or_404
from .models import Menu, Booking, Category
from .serializers import MenuSerializer, BookingSerializer, CategorySerializer
from rest_framework.permissions import AllowAny
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from .models import Cart, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
import json
from .models import Booking



# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views


# def menu(request):
#     menu_data = Menu.objects.all().order_by('name')  # 获取所有菜单项
#     main_data = {"menu": menu_data}
#     return render(request, "menu.html", main_data)  # 渲染 `menu.html`
# ✅ **修改 menu() 视图** -> 让其支持 API
@api_view(['GET'])
@permission_classes([AllowAny])
def menu(request):
    if request.META.get('HTTP_ACCEPT') == 'application/json':
        menu_items = Menu.objects.all().order_by('name')
        serializer = MenuSerializer(menu_items, many=True)
        return Response(serializer.data)

    # 如果是普通 HTML 请求，则渲染页面
    menu_data = Menu.objects.all().order_by('name')
    return render(request, "menu.html", {"menu": menu_data})


# def display_menu_item(request, pk=None):
#     if pk:
#         menu_item = get_object_or_404(Menu, pk=pk)
#     else:
#         menu_item = None
#     return render(request, "menu_item.html", {"menu_item": menu_item})

# ✅ **修改 display_menu_item() 视图**
@api_view(['GET'])
@permission_classes([AllowAny])
def display_menu_item(request, pk=None):
    menu_item = get_object_or_404(Menu, pk=pk)

    if request.META.get('HTTP_ACCEPT') == 'application/json':
        serializer = MenuSerializer(menu_item)
        return Response(serializer.data)

    # 如果是普通 HTML 请求，则渲染页面
    return render(request, "menu_item.html", {"menu_item": menu_item})

# ✅ **使用 ViewSet 管理 API**
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by('name')
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # 过滤 & 排序
    filterset_fields = ['category']  # 按分类过滤
    ordering_fields = ['price']  # 按价格排序

    def get_permissions(self):
        """
        定义不同角色的权限：
        - 所有人（包括未登录用户）可以 `GET` 所有菜单项
        - `Customer` 和 `Delivery Crew` 只能 `GET`，不能修改
        - 只有 `Manager` 才能 `POST`, `PUT`, `PATCH`, `DELETE`
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # 允许所有人 GET

        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='Manager').exists():
            return [permissions.IsAuthenticated()]  # Manager 允许修改

        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]  # 其他人禁止修改


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]



from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group

# ✅ 获取所有 Manager 用户
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])  # 只有 Manager 可以访问
def list_managers(request):
    managers = User.objects.filter(groups__name='Manager')
    return Response([user.username for user in managers])

# ✅ 添加用户到 Manager 组
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_manager(request):
    try:
        user = User.objects.get(username=request.data['username'])
        manager_group = Group.objects.get(name='Manager')
        user.groups.add(manager_group)
        return Response({"message": f"{user.username} added to Manager group"}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# ✅ 删除用户从 Manager 组
@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def remove_manager(request, userId):
    try:
        user = User.objects.get(id=userId)
        manager_group = Group.objects.get(name='Manager')
        user.groups.remove(manager_group)
        return Response({"message": f"{user.username} removed from Manager group"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# ✅ 获取所有 Delivery Crew 用户
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def list_delivery_crew(request):
    crew = User.objects.filter(groups__name='Delivery Crew')
    return Response([user.username for user in crew])

# ✅ 添加用户到 Delivery Crew 组
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def add_delivery_crew(request):
    try:
        user = User.objects.get(username=request.data['username'])
        crew_group = Group.objects.get(name='Delivery Crew')
        user.groups.add(crew_group)
        return Response({"message": f"{user.username} added to Delivery Crew group"}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# ✅ 删除用户从 Delivery Crew 组
@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
def remove_delivery_crew(request, userId):
    try:
        user = User.objects.get(id=userId)
        crew_group = Group.objects.get(name='Delivery Crew')
        user.groups.remove(crew_group)
        return Response({"message": f"{user.username} removed from Delivery Crew group"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)




# ✅ 获取当前用户的购物车
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data)

# ✅ 添加菜单项到购物车
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    data = request.data.copy()
    data['user'] = request.user.id  # 绑定当前用户
    serializer = CartSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ 清空购物车
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)

# ✅ 获取当前用户的订单
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# ✅ `Customer` 创建订单 (从购物车提交订单)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    # 创建订单
    order = Order.objects.create(user=request.user, status=0)

    # 复制购物车内容到订单
    for item in cart_items:
        OrderItem.objects.create(order=order, menu_item=item.menu_item, quantity=item.quantity)

    # 清空购物车
    cart_items.delete()

    return Response({"message": "Order created"}, status=status.HTTP_201_CREATED)

# ✅ `Manager` 获取所有订单
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_all_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# ✅ `Manager` 处理订单 (分配 Delivery Crew)
@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def update_order(request, orderId):
    try:
        order = Order.objects.get(id=orderId)
        order.delivery_crew = request.data.get("delivery_crew")  # 分配送货员
        order.status = request.data.get("status")  # 更新订单状态
        order.save()
        return Response({"message": "Order updated"}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def set_item_of_the_day(request, menu_id):
    try:
        menu_item = Menu.objects.get(id=menu_id)
        menu_item.is_item_of_the_day = request.data.get("is_item_of_the_day", True)
        menu_item.save()
        return Response({"message": f"{menu_item.name} is now Item of the Day"}, status=status.HTTP_200_OK)
    except Menu.DoesNotExist:
        return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)


# ✅ `Delivery Crew` 更新订单状态
@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_order_status(request, orderId):
    try:
        order = Order.objects.get(id=orderId, delivery_crew=request.user)
        order.status = request.data.get("status")
        order.save()
        return Response({"message": "Order status updated"}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found or not assigned to you"}, status=status.HTTP_404_NOT_FOUND)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


# @csrf_exempt
# def bookings(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#
#             # 确保请求数据包含必要字段
#             required_fields = ["first_name", "reservation_date", "reservation_slot"]
#             if not all(field in data for field in required_fields):
#                 return JsonResponse({"error": "Missing required fields"}, status=400)
#
#             # 检查该时间段是否已被预订
#             exist = Booking.objects.filter(
#                 reservation_date=data["reservation_date"],
#                 reservation_slot=data["reservation_slot"]
#             ).exists()
#
#             if not exist:
#                 booking = Booking(
#                     first_name=data["first_name"],
#                     last_name=data.get("last_name", ""),  # 如果没有提供 last_name，默认为空
#                     guest_number=data.get("guest_number", 1),  # 如果没有提供 guest_number，默认为 1
#                     comment=data.get("comment", ""),  # 如果没有提供 comment，默认为空
#                     reservation_date=data["reservation_date"],
#                     reservation_slot=data["reservation_slot"]
#                 )
#                 booking.save()
#                 return JsonResponse({"success": 1})  # 返回成功信息
#             else:
#                 return JsonResponse({"error": "Time slot already booked"}, status=400)
#
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
#
#     # 处理 GET 请求，返回预订信息
#     date_str = request.GET.get("date", None)
#     if not date_str:
#         date = datetime.today().date()
#     else:
#         try:
#             date = datetime.strptime(date_str, "%Y-%m-%d").date()
#         except ValueError:
#             return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
#
#     bookings = Booking.objects.filter(reservation_date=date)
#     booking_json = serializers.serialize("json", bookings)
#
#     return HttpResponse(booking_json, content_type="application/json")



@csrf_exempt  # 允许不带 CSRF 令牌的请求
def bookings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # 确保请求数据包含必要字段
            required_fields = ["first_name", "reservation_date", "reservation_slot"]
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # 检查该时间段是否已被预订
            exist = Booking.objects.filter(
                reservation_date=data["reservation_date"],
                reservation_slot=data["reservation_slot"]
            ).exists()

            if not exist:
                booking = Booking(
                    first_name=data["first_name"],
                    last_name=data.get("last_name", ""),  # 如果没有提供 last_name，默认为空
                    guest_number=data.get("guest_number", 1),  # 如果没有提供 guest_number，默认为 1
                    comment=data.get("comment", ""),  # 如果没有提供 comment，默认为空
                    reservation_date=data["reservation_date"],
                    reservation_slot=data["reservation_slot"]
                )
                booking.save()
                return JsonResponse({"success": 1})  # 返回成功信息
            else:
                return JsonResponse({"error": "Time slot already booked"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    # 处理 GET 请求，返回预订信息
    date_str = request.GET.get("date", None)
    if not date_str:
        date = datetime.today().date()
    else:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

    bookings = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize("json", bookings)

    return HttpResponse(booking_json, content_type="application/json")
