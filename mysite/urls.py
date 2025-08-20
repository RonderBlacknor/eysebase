
from django.contrib import admin
from django.urls import path

from movies.views import *
from django.urls import path, include

from mysite import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls'))
]

handler404 = pageNotFound # Для ошибки

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
