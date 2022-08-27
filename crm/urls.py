from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView


urlpatterns = [
    path("", include("app_crm.urls"), name='index'),
    path("robots.txt", TemplateView.as_view(template_name="robots/robots.txt", content_type="text/plain")),
    path("util/native/admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
