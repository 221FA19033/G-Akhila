from django.urls import path
from . import views

# Web pages
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/increase/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/confirm/', views.confirm_order, name='confirm_order'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
]

# API endpoints
api_urlpatterns = [
    path('login/', views.api_login, name='api_login'),
    path('products/', views.api_products, name='api_products'),
     path('cart/', views.api_cart, name='api_cart'),
    
]
