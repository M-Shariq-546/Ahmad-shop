from shop_cart.cart import Cart

def cart_context(request):
    cart = Cart(request)
    return {'total_quantity': cart.get_total_quantity(), 'cart_products': cart.get_prods()}