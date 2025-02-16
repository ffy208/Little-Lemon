from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import list_managers, add_manager, list_delivery_crew, add_delivery_crew, remove_manager, \
    remove_delivery_crew, get_cart, add_to_cart, clear_cart, get_orders, create_order, get_all_orders, \
    update_order, update_order_status, CategoryViewSet, set_item_of_the_day

# Django REST Framework 路由
router = DefaultRouter()
router.register(r'api/menu-items', views.MenuViewSet)  # RESTful API 端点
router.register(r'api/bookings', views.BookingViewSet)  # 预定 API 端点
router.register(r'api/categories', CategoryViewSet)


# urlpatterns = [
#     path('', views.home, name="home"),
#     path('about/', views.about, name="about"),
#     path('book/', views.book, name="book"),
#     # Add the remaining URL path configurations here
#     path("menu/", views.menu, name="menu"),
#     path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),
# ]

urlpatterns = [
    # HTML 视图
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('menu/', views.menu, name="menu"),  # 兼容 JSON + HTML
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  # 兼容 JSON + HTML

    # API 端点
    path('', include(router.urls)),  # 自动管理 API 端点
    path('api/groups/manager/users/', list_managers),
    path('api/groups/manager/users/add/', add_manager),
    path('api/groups/manager/users/<int:userId>/', remove_manager),
    path('api/groups/delivery-crew/users/', list_delivery_crew),
    path('api/groups/delivery-crew/users/add/', add_delivery_crew),
    path('api/groups/delivery-crew/users/<int:userId>/', remove_delivery_crew),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),  # 处理 Token 认证

    # 购物车
    path('api/cart/menu-items/', get_cart),
    path('api/cart/menu-items/add/', add_to_cart),
    path('api/cart/menu-items/clear/', clear_cart),

    # 订单
    path('api/orders/', get_orders),
    path('api/orders/create/', create_order),
    path('api/orders/all/', get_all_orders),
    path('api/orders/<int:orderId>/update/', update_order),
    path('api/orders/<int:orderId>/status/', update_order_status),
    path('api/menu-items/<int:menu_id>/item-of-the-day/', set_item_of_the_day),
    path('bookings/', views.bookings, name="bookings"),
]