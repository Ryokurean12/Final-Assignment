from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def home(request):
    query = request.GET.get('q') # Merit: Search Functionality
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'market/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'market/detail.html', {'product': product})

def add_to_cart(request, pk): # Uses POST request
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(pk)] = cart.get(str(pk), 0) + 1
        request.session['cart'] = cart
        return redirect('cart')
    return redirect('product_detail', pk=pk)

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(pk__in=cart.keys())
    cart_items, total = [], 0
    for product in products:
        quantity = cart[str(product.pk)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'market/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, pk): # Remove items from cart
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('cart')

def checkout(request): # Simulated checkout
    request.session['cart'] = {} # Cart is cleared
    return render(request, 'market/checkout.html') # Order confirmation