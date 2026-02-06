"""Template Dashboards serializers."""
from rest_framework import serializers
from .models import DashboardTemplate, TemplateInstance, FeaturedTemplate, VariableCatalog


class DashboardTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'downloads']
        extra_kwargs = {
            'category': {'required': False, 'default': 'custom'},
            'layout': {'required': False},
            'widgets': {'required': False},
        }


class DashboardTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardTemplate
        fields = ['id', 'name', 'description', 'category', 'thumbnail', 'is_official', 'downloads']


class TemplateInstanceSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    

    
    class Meta:
        model = TemplateInstance
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class FeaturedTemplateSerializer(serializers.ModelSerializer):
    template = DashboardTemplateListSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(
        queryset=DashboardTemplate.objects.all(),
        source='template',
        write_only=True,
        required=False
    )

    def create(self, validated_data):
        # Compatibility: Check if 'template' was passed as ID in initial data
        template_val = self.initial_data.get('template')
        if template_val and not validated_data.get('template'):
            if isinstance(template_val, int):
                validated_data['template'] = DashboardTemplate.objects.get(pk=template_val)
        return super().create(validated_data)
    
    class Meta:
        model = FeaturedTemplate
        fields = ['id', 'template', 'template_id', 'order', 'promo_banner', 'created_at']
        read_only_fields = ['id', 'created_at']


class VariableCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableCatalog
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
