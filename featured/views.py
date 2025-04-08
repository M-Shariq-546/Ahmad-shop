from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.http import JsonResponse
from .featured import Featured
from django.templatetags.static import static

def featured_summary(request):
    return render(request, 'featured/featured_summary.html')

# def featured_add(request):
#     featured = Featured(request)

#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         product = get_object_or_404(Product, id=product_id)
#         featured.add(product=product)

#         return JsonResponse({'message': 'Product added', 'product_id': product_id})

def featured_add(request):
    featured = Featured(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        featured.add(product=product)

        return JsonResponse({'message': 'Product added', 'product_id': product_id, 'in_favorites': True})

# def featured_delete(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')

#         if not product_id:
#             return JsonResponse({'error': 'Missing product_id'}, status=400)

#         featured = Featured(request)
#         featured.delete(product=product_id)

#         return JsonResponse({'message': 'Product removed', 'product_id': product_id})

def featured_delete(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        if not product_id:
            return JsonResponse({'error': 'Missing product_id'}, status=400)

        featured = Featured(request)
        featured.delete(product=product_id)

        return JsonResponse({'message': 'Product removed', 'product_id': product_id, 'in_favorites': False})
