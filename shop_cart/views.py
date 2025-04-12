from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.http import JsonResponse
from .cart import Cart
import json , requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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


@csrf_exempt
def send_to_telegram_view(request):
    if request.method == 'POST':
        print('====== request body', request.body)
        try:
            received_data = json.loads(request.body)
            contact_details = received_data.get('contact', {})
            cart_items = received_data.get('cart', [])

            print(cart_items)

            # Prepare the message for Telegram
            message = f"New Order Details:\n\nContact Information:\nName: {contact_details.get('name')}\nSurname: {contact_details.get('surname')}\nNumber: {contact_details.get('number')}\nAddress: {contact_details.get('address')}\n\nOrdered Items:\n"

            # Include details about the selected products
            for item in cart_items:
                product_name = item.get('name', '')
                product_price = item.get('price', 0.0)
                product_quantity = item.get('quantity', 0)

                message += f"Product: {product_name}\nPrice: ${product_price}\nQuantity: {product_quantity}\n\n"

            # Send message to Telegram
            send_to_telegram(message)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'Error processing the order: {str(e)}')  # Debug print
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })


def send_to_telegram(message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHANNEL_ID

    telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
    }

    response = requests.post(telegram_api_url, params=params)

    if response.status_code != 200:
        print(
            f"Failed to send message to Telegram. Status code: {response.status_code}"
        )


def checkout(request):
    cart_data = request.session.get('session_key', {})
    print('===== cart items ', cart_data)
    products = []
    total_price = 0

    for item_id, item in cart_data.items():
        item_total = float(item['price']) * item['quantity']
        total_price += item_total
        print('total ==== ', total_price)
        products.append({
            'id': item_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': f"{item_total:.2f}"
        })

    return render(request, 'shop_cart/checkout.html', {
        'cart_products': products,
        'total': f"{total_price:.2f}",
    })