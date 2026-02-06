"""
Dashboard Template Import/Export Service for Observer-Eye Platform.

Handles:
- Export templates to JSON format
- Import templates from JSON
- Template versioning
- Template cloning and customization
"""
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from django.utils import timezone

logger = logging.getLogger(__name__)


class TemplateExportError(Exception):
    """Error during template export."""
    pass


class TemplateImportError(Exception):
    """Error during template import."""
    pass


class TemplateValidator:
    """Validates template structure and content."""
    
    REQUIRED_FIELDS = ['name', 'category', 'layout', 'widgets']
    VALID_CATEGORIES = ['overview', 'infrastructure', 'application', 'security', 'performance', 'custom']
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> List[str]:
        """
        Validate template data structure.
        
        Args:
            data: Template data dict
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Validate category
        if 'category' in data and data['category'] not in cls.VALID_CATEGORIES:
            errors.append(f"Invalid category: {data['category']}. Must be one of {cls.VALID_CATEGORIES}")
        
        # Validate widgets
        if 'widgets' in data:
            if not isinstance(data['widgets'], list):
                errors.append("widgets must be a list")
            else:
                for i, widget in enumerate(data['widgets']):
                    widget_errors = cls._validate_widget(widget, i)
                    errors.extend(widget_errors)
        
        # Validate layout
        if 'layout' in data:
            if not isinstance(data['layout'], dict):
                errors.append("layout must be a dict")
        
        return errors
    
    @classmethod
    def _validate_widget(cls, widget: Dict[str, Any], index: int) -> List[str]:
        """Validate a single widget definition."""
        errors = []
        
        if not isinstance(widget, dict):
            return [f"Widget {index}: must be a dict"]
        
        if 'type' not in widget:
            errors.append(f"Widget {index}: missing 'type' field")
        
        if 'id' not in widget:
            errors.append(f"Widget {index}: missing 'id' field")
        
        return errors


class TemplateExporter:
    """Exports dashboard templates to portable format."""
    
    EXPORT_VERSION = "1.0"
    
    def export_template(self, template_id: str) -> Dict[str, Any]:
        """
        Export a single template to JSON-serializable dict.
        
        Args:
            template_id: UUID of the template
            
        Returns:
            Dict representing the template
        """
        from .models import DashboardTemplate
        
        try:
            template = DashboardTemplate.objects.get(id=template_id, is_active=True)
        except DashboardTemplate.DoesNotExist:
            raise TemplateExportError(f"Template not found: {template_id}")
        
        return self._template_to_dict(template)
    
    def export_templates(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Export multiple templates.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of template dicts
        """
        from .models import DashboardTemplate
        
        queryset = DashboardTemplate.objects.filter(is_active=True)
        if category:
            queryset = queryset.filter(category=category)
        
        return [self._template_to_dict(t) for t in queryset]
    
    def _template_to_dict(self, template) -> Dict[str, Any]:
        """Convert template model to export dict."""
        return {
            '_export_version': self.EXPORT_VERSION,
            '_exported_at': timezone.now().isoformat(),
            '_source': 'observer-eye',
            'id': str(template.id),
            'name': template.name,
            'description': template.description,
            'category': template.category,
            'version': template.version,
            'layout': template.layout,
            'widgets': template.widgets,
            'variables': template.variables,
            'is_official': template.is_official,
        }
    
    def export_to_json(self, template_id: str, pretty: bool = True) -> str:
        """Export template as JSON string."""
        data = self.export_template(template_id)
        if pretty:
            return json.dumps(data, indent=2, default=str)
        return json.dumps(data, default=str)


class TemplateImporter:
    """Imports dashboard templates from external sources."""
    
    def import_template(
        self,
        data: Dict[str, Any],
        user_id: str = None,
        allow_overwrite: bool = False,
    ) -> 'DashboardTemplate':
        """
        Import a template from dict data.
        
        Args:
            data: Template data dict
            user_id: Optional user ID for tracking
            allow_overwrite: Whether to update existing template with same name
            
        Returns:
            Created or updated DashboardTemplate
        """
        from .models import DashboardTemplate
        
        # Validate
        errors = TemplateValidator.validate(data)
        if errors:
            raise TemplateImportError(f"Validation errors: {'; '.join(errors)}")
        
        # Check for existing
        existing = DashboardTemplate.objects.filter(name=data['name'], is_active=True).first()
        
        if existing and not allow_overwrite:
            raise TemplateImportError(f"Template with name '{data['name']}' already exists")
        
        if existing and allow_overwrite:
            return self._update_template(existing, data)
        
        return self._create_template(data)
    
    def _create_template(self, data: Dict[str, Any]) -> 'DashboardTemplate':
        """Create a new template from import data."""
        from .models import DashboardTemplate
        
        template = DashboardTemplate.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            category=data['category'],
            version=data.get('version', '1.0.0'),
            layout=data.get('layout', {}),
            widgets=data.get('widgets', []),
            variables=data.get('variables', []),
            is_official=False,  # Imported templates are never official
        )
        
        logger.info(f"Imported new template: {template.name} ({template.id})")
        return template
    
    def _update_template(self, template, data: Dict[str, Any]) -> 'DashboardTemplate':
        """Update existing template with import data."""
        template.description = data.get('description', template.description)
        template.category = data.get('category', template.category)
        template.version = data.get('version', template.version)
        template.layout = data.get('layout', template.layout)
        template.widgets = data.get('widgets', template.widgets)
        template.variables = data.get('variables', template.variables)
        template.save()
        
        logger.info(f"Updated template: {template.name} ({template.id})")
        return template
    
    def import_from_json(
        self,
        json_string: str,
        user_id: str = None,
        allow_overwrite: bool = False,
    ) -> 'DashboardTemplate':
        """Import template from JSON string."""
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise TemplateImportError(f"Invalid JSON: {e}")
        
        return self.import_template(data, user_id, allow_overwrite)
    
    def import_bulk(
        self,
        templates: List[Dict[str, Any]],
        user_id: str = None,
        allow_overwrite: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Import multiple templates.
        
        Returns:
            List of results with status for each template
        """
        results = []
        
        for data in templates:
            try:
                template = self.import_template(data, user_id, allow_overwrite)
                results.append({
                    'name': data.get('name'),
                    'status': 'success',
                    'template_id': str(template.id),
                })
            except TemplateImportError as e:
                results.append({
                    'name': data.get('name'),
                    'status': 'error',
                    'error': str(e),
                })
        
        return results


class TemplateCloner:
    """Clones and customizes dashboard templates."""
    
    def clone_template(
        self,
        template_id: str,
        user_id: str,
        new_name: str = None,
        customizations: Dict[str, Any] = None,
    ) -> 'TemplateInstance':
        """
        Clone a template for user customization.
        
        Args:
            template_id: Source template UUID
            user_id: User ID
            new_name: Optional new name for the clone
            customizations: Initial customizations
            
        Returns:
            TemplateInstance with cloned content
        """
        from .models import DashboardTemplate, TemplateInstance
        
        try:
            template = DashboardTemplate.objects.get(id=template_id, is_active=True)
        except DashboardTemplate.DoesNotExist:
            raise TemplateExportError(f"Template not found: {template_id}")
        
        # Increment download counter
        template.downloads += 1
        template.save(update_fields=['downloads'])
        
        # Create instance
        instance = TemplateInstance.objects.create(
            template=template,
            user_id=user_id,
            name=new_name or f"{template.name} (Copy)",
            variable_values={},
            customizations=customizations or {},
        )
        
        logger.info(f"Cloned template {template.name} for user {user_id}")
        return instance
    
    def apply_customizations(
        self,
        instance_id: str,
        customizations: Dict[str, Any],
    ) -> 'TemplateInstance':
        """
        Apply customizations to a template instance.
        
        Args:
            instance_id: Template instance UUID
            customizations: Customization dict
            
        Returns:
            Updated TemplateInstance
        """
        from .models import TemplateInstance
        
        try:
            instance = TemplateInstance.objects.get(id=instance_id, is_active=True)
        except TemplateInstance.DoesNotExist:
            raise TemplateExportError(f"Instance not found: {instance_id}")
        
        # Merge customizations
        current = instance.customizations or {}
        current.update(customizations)
        instance.customizations = current
        instance.save()
        
        return instance


# Service facade
class TemplateService:
    """
    Main service for dashboard template operations.
    
    Usage:
        service = TemplateService()
        
        # Export
        json_data = service.export_template_json(template_id)
        
        # Import
        template = service.import_template_json(json_string)
        
        # Clone
        instance = service.clone_for_user(template_id, user_id)
    """
    
    def __init__(self):
        self.exporter = TemplateExporter()
        self.importer = TemplateImporter()
        self.cloner = TemplateCloner()
    
    def export_template_json(self, template_id: str, pretty: bool = True) -> str:
        """Export template as JSON string."""
        return self.exporter.export_to_json(template_id, pretty)
    
    def export_templates(self, category: str = None) -> List[Dict[str, Any]]:
        """Export multiple templates as list of dicts."""
        return self.exporter.export_templates(category)
    
    def import_template_json(
        self,
        json_string: str,
        user_id: str = None,
        allow_overwrite: bool = False,
    ):
        """Import template from JSON string."""
        return self.importer.import_from_json(json_string, user_id, allow_overwrite)
    
    def import_templates_bulk(
        self,
        templates: List[Dict[str, Any]],
        user_id: str = None,
    ) -> List[Dict[str, Any]]:
        """Bulk import templates."""
        return self.importer.import_bulk(templates, user_id)
    
    def clone_for_user(
        self,
        template_id: str,
        user_id: str,
        name: str = None,
    ):
        """Clone a template for a user."""
        return self.cloner.clone_template(template_id, user_id, name)
    
    def validate_template(self, data: Dict[str, Any]) -> List[str]:
        """Validate template data."""
        return TemplateValidator.validate(data)
