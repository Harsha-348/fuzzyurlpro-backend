"""
URL configuration for fuzzyurlpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from urlshortener.views import home, api_health_check, ShortenURLAPIView, redirect_to_original, analytics_view

urlpatterns = [
    path('', home, name='home'),  # Home Page
    path('admin/', admin.site.urls),  # Admin Panel
    path('api/', api_health_check, name='api-root'),
    path('api/health/', api_health_check, name='api-health-check'),  # ✅ Global API health check
    path('api/shorten/', ShortenURLAPIView.as_view(), name='shorten-url'),  # ✅ Shorten URL API
    path('api/analytics/<str:short_code>/', analytics_view, name='analytics'),  # ✅ Analytics endpoint
    path('<str:short_code>/', redirect_to_original, name='redirect-to-original'),  # ✅ Redirect to original URL
]

# Serve media files (QR codes) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

