from django.urls import path
from .views import cart_add, cart_summary, cart_delete, checkout, send_to_telegram, send_to_telegram_view

app_name = 'shop_cart'

urlpatterns = [
    path('', cart_summary, name='cart_summary'),
    path('add/', cart_add, name='cart_add'),
    path('delete/', cart_delete, name='cart_delete'),
    path('checkout/', checkout, name='checkout'),
    path('send-to-telegram/', send_to_telegram_view, name='send-to-telegram'),
]
