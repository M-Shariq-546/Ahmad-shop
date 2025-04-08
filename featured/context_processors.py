from featured.featured import Featured

def featured_context(request):
    featured = Featured(request)
    return {'featured_total_quantity': featured.get_total_quantity(), 'featured_products': featured.get_prods()}