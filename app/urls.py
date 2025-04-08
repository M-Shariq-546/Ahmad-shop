from django.urls import path
from .views import HomeView, get_subcategories, CategoryListView, CategoryDetailView, search

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('get-subcategories/', get_subcategories, name='get_subcategories'),
    path('categories/', CategoryListView.as_view(), name='categories_list'),
    path('category/<slug:category_slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('search/', search, name='search'),
]
