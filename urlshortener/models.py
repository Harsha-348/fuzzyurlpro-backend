from django.db import models
from django.utils.crypto import get_random_string
from datetime import datetime
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings

# --- ShortURL Model ---
class ShortURL(models.Model):
    original_url = models.URLField()
    shortened_url = models.CharField(max_length=15, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    click_count = models.PositiveIntegerField(default=0)
    password = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
    
        if not self.shortened_url:
            self.shortened_url = get_random_string(length=6)
    
        if is_new and not self.qr_code:
            self.generate_qr_code()
    
        super().save(*args, **kwargs)  # Save after QR code generation

    def generate_qr_code(self):
        qr_data = self.get_full_short_url()
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f"{self.shortened_url}_qr.png"
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()

    def get_full_short_url(self):
        domain = getattr(settings, 'SITE_DOMAIN', 'http://127.0.0.1:8000')
        return f"{domain}/{self.shortened_url}"

    def is_expired(self):
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False

    def __str__(self):
        return f"{self.original_url} → {self.shortened_url}"

# --- ClickAnalytics Model ---
class ClickAnalytics(models.Model):
    short_url = models.ForeignKey('ShortURL', related_name='clicks', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # This is the missing field
    browser = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
