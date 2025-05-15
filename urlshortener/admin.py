# Register your models here.
from django.contrib import admin
from .models import ShortURL, ClickAnalytics

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'shortened_url', 'click_count', 'created_at', 'expires_at')
    search_fields = ('original_url', 'shortened_url')

class ClickAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'browser', 'device', 'timestamp', 'location')  # Updated field names

admin.site.register(ClickAnalytics, ClickAnalyticsAdmin)
