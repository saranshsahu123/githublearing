from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from resume import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_resume, name='upload_resume'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
