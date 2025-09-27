from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Cart
from django.db.models import Q

# LOGIN
def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')

# REGISTER
def user_register(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "User registered successfully")
            return redirect('login')
    return render(request, 'register.html')

# PRODUCT LIST WITH SEARCH
@login_required(login_url='login')
def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# ADD PRODUCT
@login_required(login_url='login')
def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        Product.objects.create(name=name, price=price, description=description)
        messages.success(request, "Product added successfully")
        return redirect('dashboard')
    return render(request, 'add_product.html')

# UPDATE PRODUCT
@login_required(login_url='login')
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description', '')
        product.save()
        messages.success(request, "Product updated successfully")
        return redirect('dashboard')
    return render(request, 'update_product.html', {'product': product})

# DELETE PRODUCT
@login_required(login_url='login')
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, "Product deleted successfully")
    return redirect('dashboard')

# DASHBOARD (Admin)
@login_required(login_url='login')
def dashboard(request):
    total_products = Product.objects.count()
    total_users = User.objects.count()

    # Search functionality
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'admin_dashboard.html', {
        'total_products': total_products,
        'total_users': total_users,
        'products': products
    })


# CART
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    total = 0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        total += item.total_price

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })



# ADD TO CART
@login_required(login_url='login')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart")
    return redirect('product_list')

# Increase quantity
@login_required(login_url='login')
def increase_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

# Decrease quantity
@login_required(login_url='login')
def decrease_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # If quantity is 1 and user decreases, remove from cart
    return redirect('cart')

# Delete item from cart
@login_required(login_url='login')
def delete_cart_item(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')


# USER MANAGEMENT (Admin)
@login_required(login_url='login')
def manage_users(request):
    users = User.objects.all()

    # Add user
    if request.method == "POST" and 'add_user' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "User added successfully")
            return redirect('manage_users')

    return render(request, 'manage_users.html', {'users': users})

# DELETE USER
@login_required(login_url='login')
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if not user.is_superuser:
        user.delete()
        messages.success(request, "User deleted successfully")
    else:
        messages.error(request, "Cannot delete superuser")
    return redirect('manage_users')
