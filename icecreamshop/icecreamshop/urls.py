from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from icecream_tubs.urls import icecreams_router
from orders.urls import orders_router

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("", include(icecreams_router.urls)),
                  path("", include(orders_router.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
