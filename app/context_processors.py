from products.models import Category
from django.db.models import Exists, OuterRef

def categories(request):
    parent_categories = Category.objects.filter(parent__isnull=True).annotate(
        has_subcategories=Exists(Category.objects.filter(parent=OuterRef('pk')))
    )
    return {'parent_categories': parent_categories}
