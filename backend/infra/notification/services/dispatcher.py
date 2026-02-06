"""
Notification Dispatcher Service for Observer-Eye Platform.

Handles alert delivery across multiple channels:
- Email (SMTP)
- Slack
- Webhook
- PagerDuty
- Microsoft Teams
- SMS (via Twilio/other providers)
"""
import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.template import Template, Context
from django.utils import timezone

logger = logging.getLogger(__name__)


class NotificationError(Exception):
    """Base exception for notification errors."""
    pass


class ChannelDispatcher(ABC):
    """Abstract base class for notification channel dispatchers."""
    
    @abstractmethod
    def dispatch(self, alert: 'Alert', channel_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch an alert through this channel.
        
        Args:
            alert: The alert to send
            channel_config: Channel-specific configuration
            
        Returns:
            Dict with 'success' boolean and optional 'message'
        """
        raise NotImplementedError("Subclasses must implement dispatch()")
    
    def format_message(self, alert: 'Alert', template: Optional[str] = None) -> str:
        """Format alert message using template if provided."""
        if template:
            t = Template(template)
            c = Context({
                'alert': alert,
                'severity': alert.severity,
                'name': alert.name,
                'message': alert.message,
                'labels': alert.labels,
                'annotations': alert.annotations,
                'started_at': alert.started_at,
            })
            return t.render(c)
        
        return f"[{alert.severity.upper()}] {alert.name}: {alert.message}"


class EmailDispatcher(ChannelDispatcher):
    """Email notification dispatcher using Django's email backend."""
    
    def dispatch(self, alert, channel_config: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert via email."""
        try:
            recipients = channel_config.get('recipients', [])
            subject_template = channel_config.get('subject', '[Observer-Eye Alert] {{ name }}')
            body_template = channel_config.get('body')
            
            if not recipients:
                return {'success': False, 'message': 'No recipients configured'}
            
            subject = self.format_message(alert, subject_template)
            body = self.format_message(alert, body_template)
            
            send_mail(
                subject=subject,
                message=body,
                from_email=channel_config.get('from_email', settings.DEFAULT_FROM_EMAIL),
                recipient_list=recipients,
                fail_silently=False,
            )
            
            return {'success': True, 'message': f'Email sent to {len(recipients)} recipients'}
            
        except Exception as e:
            logger.error(f"Email dispatch failed: {e}")
            return {'success': False, 'message': str(e)}


class WebhookDispatcher(ChannelDispatcher):
    """Generic webhook notification dispatcher."""
    
    def dispatch(self, alert, channel_config: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert via webhook."""
        import requests  # Lazy import
        
        try:
            url = channel_config.get('url')
            if not url:
                return {'success': False, 'message': 'Webhook URL not configured'}
            
            method = channel_config.get('method', 'POST').upper()
            headers = channel_config.get('headers', {'Content-Type': 'application/json'})
            
            payload = {
                'alert_id': str(alert.id),
                'name': alert.name,
                'severity': alert.severity,
                'state': alert.state,
                'message': alert.message,
                'labels': alert.labels,
                'annotations': alert.annotations,
                'started_at': alert.started_at.isoformat() if alert.started_at else None,
                'resolved_at': alert.resolved_at.isoformat() if alert.resolved_at else None,
            }
            
            # Merge with custom payload if provided
            custom_payload = channel_config.get('payload', {})
            payload.update(custom_payload)
            
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                headers=headers,
                timeout=channel_config.get('timeout', 10),
            )
            response.raise_for_status()
            
            return {'success': True, 'message': f'Webhook delivered (HTTP {response.status_code})'}
            
        except Exception as e:
            logger.error(f"Webhook dispatch failed: {e}")
            return {'success': False, 'message': str(e)}


class SlackDispatcher(ChannelDispatcher):
    """Slack notification dispatcher using incoming webhooks."""
    
    SEVERITY_COLORS = {
        'info': '#36a64f',
        'warning': '#ffcc00',
        'error': '#ff6600',
        'critical': '#ff0000',
    }
    
    def dispatch(self, alert, channel_config: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert to Slack."""
        import requests  # Lazy import
        
        try:
            webhook_url = channel_config.get('webhook_url')
            if not webhook_url:
                return {'success': False, 'message': 'Slack webhook URL not configured'}
            
            color = self.SEVERITY_COLORS.get(alert.severity, '#808080')
            
            payload = {
                'attachments': [{
                    'color': color,
                    'title': f"{alert.state.upper()}: {alert.name}",
                    'text': alert.message,
                    'fields': [
                        {'title': 'Severity', 'value': alert.severity.upper(), 'short': True},
                        {'title': 'State', 'value': alert.state.upper(), 'short': True},
                        {'title': 'Started', 'value': alert.started_at.strftime('%Y-%m-%d %H:%M:%S UTC') if alert.started_at else 'N/A', 'short': True},
                    ],
                    'footer': 'Observer-Eye',
                    'ts': int(alert.started_at.timestamp()) if alert.started_at else int(datetime.now().timestamp()),
                }]
            }
            
            # Add custom channel if specified
            channel = channel_config.get('channel')
            if channel:
                payload['channel'] = channel
            
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=channel_config.get('timeout', 10),
            )
            response.raise_for_status()
            
            return {'success': True, 'message': 'Slack message delivered'}
            
        except Exception as e:
            logger.error(f"Slack dispatch failed: {e}")
            return {'success': False, 'message': str(e)}


class TeamsDispatcher(ChannelDispatcher):
    """Microsoft Teams notification dispatcher using incoming webhooks."""
    
    SEVERITY_COLORS = {
        'info': '00FF00',
        'warning': 'FFFF00',
        'error': 'FFA500',
        'critical': 'FF0000',
    }
    
    def dispatch(self, alert, channel_config: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert to Microsoft Teams."""
        import requests  # Lazy import
        
        try:
            webhook_url = channel_config.get('webhook_url')
            if not webhook_url:
                return {'success': False, 'message': 'Teams webhook URL not configured'}
            
            color = self.SEVERITY_COLORS.get(alert.severity, '808080')
            
            payload = {
                '@type': 'MessageCard',
                '@context': 'http://schema.org/extensions',
                'themeColor': color,
                'summary': f"Alert: {alert.name}",
                'sections': [{
                    'activityTitle': f"🚨 {alert.state.upper()}: {alert.name}",
                    'activitySubtitle': f"Severity: {alert.severity.upper()}",
                    'text': alert.message,
                    'facts': [
                        {'name': 'State', 'value': alert.state.upper()},
                        {'name': 'Started', 'value': alert.started_at.strftime('%Y-%m-%d %H:%M:%S UTC') if alert.started_at else 'N/A'},
                    ],
                }],
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=channel_config.get('timeout', 10),
            )
            response.raise_for_status()
            
            return {'success': True, 'message': 'Teams message delivered'}
            
        except Exception as e:
            logger.error(f"Teams dispatch failed: {e}")
            return {'success': False, 'message': str(e)}


class PagerDutyDispatcher(ChannelDispatcher):
    """PagerDuty notification dispatcher using Events API v2."""
    
    SEVERITY_MAP = {
        'info': 'info',
        'warning': 'warning',
        'error': 'error',
        'critical': 'critical',
    }
    
    def dispatch(self, alert, channel_config: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert to PagerDuty."""
        import requests  # Lazy import
        
        try:
            routing_key = channel_config.get('routing_key')
            if not routing_key:
                return {'success': False, 'message': 'PagerDuty routing key not configured'}
            
            severity = self.SEVERITY_MAP.get(alert.severity, 'warning')
            event_action = 'resolve' if alert.state == 'resolved' else 'trigger'
            
            payload = {
                'routing_key': routing_key,
                'event_action': event_action,
                'dedup_key': str(alert.id),
                'payload': {
                    'summary': f"{alert.name}: {alert.message[:100]}",
                    'severity': severity,
                    'source': 'observer-eye',
                    'timestamp': alert.started_at.isoformat() if alert.started_at else timezone.now().isoformat(),
                    'custom_details': {
                        'message': alert.message,
                        'labels': alert.labels,
                        'annotations': alert.annotations,
                    },
                },
            }
            
            response = requests.post(
                'https://events.pagerduty.com/v2/enqueue',
                json=payload,
                timeout=channel_config.get('timeout', 10),
            )
            response.raise_for_status()
            
            return {'success': True, 'message': f'PagerDuty event {event_action}d'}
            
        except Exception as e:
            logger.error(f"PagerDuty dispatch failed: {e}")
            return {'success': False, 'message': str(e)}


# Dispatcher registry
DISPATCHERS = {
    'email': EmailDispatcher(),
    'webhook': WebhookDispatcher(),
    'slack': SlackDispatcher(),
    'teams': TeamsDispatcher(),
    'pagerduty': PagerDutyDispatcher(),
}


class NotificationService:
    """
    Main notification service for dispatching alerts.
    
    Usage:
        service = NotificationService()
        results = service.dispatch_alert(alert)
    """
    
    def __init__(self):
        self.dispatchers = DISPATCHERS
    
    def dispatch_alert(self, alert) -> List[Dict[str, Any]]:
        """
        Dispatch an alert to all configured channels.
        
        Args:
            alert: The Alert model instance to dispatch
            
        Returns:
            List of dispatch results for each channel
        """
        from .models import NotificationChannel, NotificationHistory
        
        results = []
        
        # Get channels from alert rule
        if hasattr(alert, 'rule') and alert.rule:
            channels = alert.rule.channels.filter(is_active=True)
        else:
            # Fallback to default channels
            channels = NotificationChannel.objects.filter(is_active=True, is_default=True)
        
        for channel in channels:
            result = self._dispatch_to_channel(alert, channel)
            results.append(result)
            
            # Record notification history
            NotificationHistory.objects.create(
                alert=alert,
                channel=channel,
                status='sent' if result['success'] else 'failed',
                sent_at=timezone.now() if result['success'] else None,
                error_message=result.get('message', '') if not result['success'] else '',
            )
        
        return results
    
    def _dispatch_to_channel(self, alert, channel) -> Dict[str, Any]:
        """Dispatch alert to a single channel."""
        dispatcher = self.dispatchers.get(channel.channel_type)
        
        if not dispatcher:
            return {
                'success': False,
                'channel': channel.name,
                'channel_type': channel.channel_type,
                'message': f"No dispatcher for channel type: {channel.channel_type}",
            }
        
        try:
            result = dispatcher.dispatch(alert, channel.config)
            return {
                'success': result.get('success', False),
                'channel': channel.name,
                'channel_type': channel.channel_type,
                'message': result.get('message', ''),
            }
        except Exception as e:
            return {
                'success': False,
                'channel': channel.name,
                'channel_type': channel.channel_type,
                'message': str(e),
            }
    
    def test_channel(self, channel) -> Dict[str, Any]:
        """Test a notification channel with a sample alert."""
        from .models import Alert
        
        # Create a mock alert for testing
        class MockAlert:
            id = 'test-alert-id'
            name = 'Test Alert'
            severity = 'info'
            state = 'firing'
            message = 'This is a test alert from Observer-Eye'
            labels = {'test': 'true'}
            annotations = {'description': 'Testing notification channel'}
            started_at = timezone.now()
            resolved_at = None
        
        return self._dispatch_to_channel(MockAlert(), channel)


# Convenience function
def dispatch_alert(alert) -> List[Dict[str, Any]]:
    """Dispatch an alert to all configured channels."""
    service = NotificationService()
    return service.dispatch_alert(alert)
