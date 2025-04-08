from django.urls import path
from .views import cart_add, cart_summary, cart_delete

app_name = 'shop_cart'

urlpatterns = [
    path('', cart_summary, name='cart_summary'),
    path('add/', cart_add, name='cart_add'),
    path('delete/', cart_delete, name='cart_delete'),
]
