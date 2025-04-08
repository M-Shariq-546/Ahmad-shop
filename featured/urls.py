from django.urls import path
from .views import featured_add, featured_summary, featured_delete

app_name = 'featured'

urlpatterns = [
    path('', featured_summary, name='featured_summary'),
    path('add/', featured_add, name='featured_add'),
    path('delete/', featured_delete, name='featured_delete'),
]
