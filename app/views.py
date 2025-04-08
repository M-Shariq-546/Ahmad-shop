from django.shortcuts import get_object_or_404, render

from django.http import JsonResponse
from products.models import Category, Product

from django.views.generic import TemplateView, ListView, DetailView

from django.db.models import Q

from django.core.paginator import Paginator

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Category.objects.filter(parent_id=category_id).values('id', 'name', 'slug')

    # Add `has_subcategories` flag
    subcategories_list = list(subcategories)
    for subcategory in subcategories_list:
        subcategory['has_subcategories'] = Category.objects.filter(parent_id=subcategory['id']).exists()

    return JsonResponse({'subcategories': subcategories_list})

from django.views.generic import TemplateView
class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newest_products'] = Product.objects.filter(in_stock=True).order_by('-id')[:16].only(
        'name', 'slug', 'price', 'discount_price', 'images', 'is_top_seller'
        )

        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """ Fetch only top-level categories (those without parents). """
        return Category.objects.filter(parent__isnull=True)

class CategoryDetailView(DetailView):
    template_name = 'category/category_detail.html'
    paginate_by = 20

    def get_object(self):
        """ Fetch category by slug. """
        category_slug = self.kwargs['category_slug']
        return get_object_or_404(Category, slug=category_slug)

    def get_queryset(self):
        queryset = Product.objects.all()
        filters = self.request.GET

        min_price = filters.get('min_price')
        max_price = filters.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        characteristic_filters = {}

        for key, values in filters.lists():
            if key in ['min_price', 'max_price', 'sort', 'page']:  # Excluding 'page' to avoid conflicts
                continue
            characteristic_filters[key] = values 

        for name, values in characteristic_filters.items():
            queryset = queryset.filter(characteristics__name=name, characteristics__value__in=values)

        sort_order = filters.get('sort')
        if sort_order == 'cheap_first':
            queryset = queryset.order_by('price')  
        elif sort_order == 'expensive_first':
            queryset = queryset.order_by('-price') 
        else:
            queryset = queryset.order_by('-published_date')

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category = self.get_object()
        product_list = self.get_queryset().filter(category=category, in_stock=True)

        # Pagination logic
        paginator = Paginator(product_list, self.paginate_by)
        page = self.request.GET.get('page')

        paginated_products = paginator.get_page(page)
        context['product_list'] = paginated_products
        context['paginator'] = paginator
        context['page_obj'] = paginated_products
        context['is_paginated'] = paginated_products.has_other_pages()

        context['subcategories'] = Category.objects.filter(parent=category)
        print(product_list)
        characteristics = {}
        for product in paginated_products:
            for characteristic in product.characteristics.all():
                if characteristic.name not in characteristics:
                    characteristics[characteristic.name] = set()
                characteristics[characteristic.name].add(characteristic.value)

        context['characteristics'] = {key: list(values) for key, values in characteristics.items()}

        return context



def search(request):
    
    if request.method == 'POST':
        q_user = request.POST.get('q', '')
        q = Product.objects.filter(Q(name__icontains=q_user) | Q(description__icontains=q_user))
        return render(request, 'pages/search.html', {'q': q, 'q_user': q_user})
    else:
        return render(request, 'pages/search.html', {})