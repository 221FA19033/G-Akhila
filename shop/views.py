from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem

# shop/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


from .models import CartItem
from .serializers import CartItemSerializer  # create serializer if not exist

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_cart(request):
    """Return all cart items for the logged-in user"""
    cart_items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)






from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username
        })
    return Response({"error": "Invalid credentials"}, status=400)

# ---------------- Authentication ----------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"✅ Welcome back, {username}!")
            return redirect('product_list')
        else:
            messages.error(request, "❌ Invalid username or password")
    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "✅ User created successfully")
            return redirect('login')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------- Home Redirect ----------------
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    return redirect('login')

# ---------------- Product Views ----------------
@login_required(login_url='/login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required(login_url='/login/')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# ---------------- Cart Views ----------------
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='/login/')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required(login_url='/login/')
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required(login_url='/login/')
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

# ---------------- Checkout ----------------
@login_required(login_url='/login/')
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')
    if request.method == "POST":
        address = request.POST.get('address')
        request.session['delivery_address'] = address
        return redirect('confirm_order')
    total_amount = sum(item.total_price() for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required(login_url='/login/')
def confirm_order(request):
    address = request.session.get('delivery_address', None)
    if not address:
        return redirect('checkout')
    # Clear cart after "payment"
    CartItem.objects.filter(user=request.user).delete()
    return render(request, 'order_confirm.html', {'address': address})

# ---------------- Customer List ----------------
@login_required(login_url='/login/')
def customer_list(request):
    customers = User.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})
