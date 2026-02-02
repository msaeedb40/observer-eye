"""Settings admin."""
from django.contrib import admin
from .models import Setting, UserPreference, FeatureFlag

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'category', 'is_sensitive', 'created_at']
    list_filter = ['category', 'is_sensitive']
    search_fields = ['key']

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'key', 'created_at']
    list_filter = ['user_id']

@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ['name', 'enabled', 'rollout_percentage', 'created_at']
    list_filter = ['enabled']
