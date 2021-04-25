from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500

from . import views


handler404 = "foodgram.views.page_not_found"
handler500 = "foodgram.views.server_error" 


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("favorites/", include("favorites.urls")),
    path("followings/", include("follows.urls")),
    path("shopping-list/", include("shopping_list.urls")),
    path("", include("recipes.urls")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:  # new
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
