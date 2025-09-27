from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Redirect root URL to login or product list
def redirect_root(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
  
    path('', include('products.urls')),
]
