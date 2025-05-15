import random
import string
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django_user_agents.utils import get_user_agent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializers import ShortURLSerializer
from .models import ShortURL, ClickAnalytics

def track_click(request, url_obj):
    ip = request.META.get('REMOTE_ADDR', '')
    user_agent = get_user_agent(request)

    device_info = user_agent.device.family
    browser_info = user_agent.browser.family

    # Example: Add location tracking if you have a GeoIP library configured
    location = "Unknown"  # Replace with actual location logic if available

    ClickAnalytics.objects.create(
        short_url=url_obj,
        ip_address=ip,
        device=device_info,
        browser=browser_info,
        location=location
    )

@method_decorator(csrf_exempt, name='dispatch')
class ShortenURLAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ShortURLSerializer(data=request.data)
        if serializer.is_valid():
            custom_alias = request.data.get("custom_alias")

            if custom_alias:
                if ShortURL.objects.filter(shortened_url=custom_alias).exists():
                    return Response({"error": "Custom alias already taken."}, status=status.HTTP_400_BAD_REQUEST)
                short_code = custom_alias
            else:
                short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                while ShortURL.objects.filter(shortened_url=short_code).exists():
                    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

            short_url_obj = ShortURL.objects.create(
                original_url=serializer.validated_data["original_url"],
                shortened_url=short_code,
                expires_at=serializer.validated_data.get("expires_at"),
                password=serializer.validated_data.get("password")
            )

            short_url = request.build_absolute_uri(f"/{short_url_obj.shortened_url}/")
            qr_code_url = request.build_absolute_uri(short_url_obj.qr_code.url) if short_url_obj.qr_code else None

            return Response({
                "short_url": short_url,
                "original_url": short_url_obj.original_url,
                "qr_code_url": qr_code_url,
                "expires_at": short_url_obj.expires_at,
                "click_count": short_url_obj.click_count,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def redirect_to_original(request, short_code):  
    url_obj = get_object_or_404(ShortURL, shortened_url=short_code)

    if url_obj.expires_at and timezone.now() > url_obj.expires_at:
        return HttpResponse("Link has expired.", status=410)

    entered_password = request.GET.get('password')
    if url_obj.password and (not entered_password or entered_password != url_obj.password):
        return HttpResponse("Incorrect password.", status=403)

    track_click(request, url_obj)
    url_obj.click_count += 1
    url_obj.save()
    
    return redirect(url_obj.original_url)

@csrf_exempt
def api_health_check(request):
    return JsonResponse({"message": "API is working"})

def home(request):
    return HttpResponse("Welcome to Fuzzy URL Shortener 🚀")

def analytics_view(request, short_code):
    url_obj = get_object_or_404(ShortURL, shortened_url=short_code)
    analytics_data = [
        {
            "timestamp": click.timestamp.isoformat(),
            "browser": click.browser,
            "device": click.device,
            "location": click.location,
        }
        for click in url_obj.clicks.all()
    ]
    return JsonResponse(analytics_data, safe=False)
