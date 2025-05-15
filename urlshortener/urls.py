from django.urls import path, re_path
from .views import ShortenURLAPIView, redirect_to_original, api_health_check, home

urlpatterns = [
    path('api/health/', api_health_check, name="api-health-check"), 
    path('api/shorten/', ShortenURLAPIView.as_view(), name='shorten-url'),  
    path('', home, name='home'),  
    re_path(r'^(?P<short_code>[a-zA-Z0-9]+)/$', redirect_to_original, name='redirect-to-original'),
]
