from rest_framework import serializers
from .models import ShortURL, ClickAnalytics
from django.utils.crypto import get_random_string
from django.utils import timezone

class ShortURLSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()
    shortened_url = serializers.CharField(required=False)

    class Meta:
        model = ShortURL
        fields = [
            'original_url', 'shortened_url', 'expires_at',
            'password', 'qr_code_url', 'click_count'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'expires_at': {'required': False},
        }

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.qr_code.url) if request else obj.qr_code.url
        return None

    def create(self, validated_data):
        if not validated_data.get('shortened_url'):
            validated_data['shortened_url'] = self.generate_unique_code()
        return super().create(validated_data)

    def generate_unique_code(self):
        while True:
            code = get_random_string(length=6)
            if not ShortURL.objects.filter(shortened_url=code).exists():
                return code

    def validate_shortened_url(self, value):
        if ShortURL.objects.filter(shortened_url=value).exists():
            raise serializers.ValidationError("This short code is already taken.")
        return value

    def validate_expires_at(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Expiration date cannot be in the past.")
        return value

class ClickAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickAnalytics
        fields = ['id', 'clicked_at', 'ip_address', 'device_info', 'browser_info']
