from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.http import JsonResponse
from .cart import Cart
from django.templatetags.static import static

def cart_summary(request):
    return render(request, 'shop_cart/cart_summary.html')

def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        
        cart.add(product)

        def get_image_url(product):
            if product.images:
                return request.build_absolute_uri(product.images.url)
            else:
                return request.build_absolute_uri(static('assets/placeholder.png'))

        cart_data = {
            'total_quantity': cart.get_total_quantity(),
            'cart_products': [
                {
                    'id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'price': str(product.price),
                    'image_url': get_image_url(product),
                    'discount_price': str(product.discount_price) if product.discount_price else '',
                    'discount_percentage': round(product.discount_percentage(), 0) if product.discount_price else None,  
                    
                }
                for product in cart.get_prods()
            ]
        }

        return JsonResponse(cart_data)
    
def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

        response = JsonResponse({'Product Name: ': product_id})

        return response