from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from drop_app import settings
# Nao mudar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('user/', include('user.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)