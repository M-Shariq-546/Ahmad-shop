from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

admin.site.site_header = "Ahmad Shop Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
]+ i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include("app.urls")),
    path('products/', include("products.urls")),
    path('cart/', include("shop_cart.urls")),
    path('featured/', include("featured.urls")),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)