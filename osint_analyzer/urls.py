from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('deepseek/', include('main.urls')),  # 👈 Ruta para el endpoint
]
