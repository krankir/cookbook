from django.contrib import admin
# from django.conf.urls.static import static
from django.urls import path, include

# from mysite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cookbook/', include('cookbook.urls')),
]

# urlpatterns += [
#         path("__debug__/", include("debug_toolbar.urls")),
#     ]
#
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

