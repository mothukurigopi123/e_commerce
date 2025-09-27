from django.urls import path
from . import views
from django.shortcuts import redirect

def redirect_root(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    return redirect('login')

urlpatterns = [
    path('', redirect_root, name='home'),  # root URL redirect
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),

    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/update/<int:id>/', views.update_product, name='update_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),

    path('cart/', views.cart, name='cart'),

    path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/delete/<int:id>/', views.delete_cart_item, name='delete_cart_item'),

    
path('manage-users/', views.manage_users, name='manage_users'),
path('users/delete/<int:id>/', views.delete_user, name='delete_user'),

]
