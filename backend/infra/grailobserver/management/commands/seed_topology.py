from django.core.management.base import BaseCommand
from grailobserver.models import GrailEntity, GrailRelationship
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed initial topology data for Grail Graph Engine'

    def handle(self, *args, **options):
        self.stdout.write('Seeding topology data...')
        
        # Clear existing data
        GrailRelationship.objects.all().delete()
        GrailEntity.objects.all().delete()
        
        # Create Entities
        entities_data = [
            {'entity_id': 'srv-frontend', 'display_name': 'frontend-v1', 'entity_type': 'service', 'health_status': 'healthy'},
            {'entity_id': 'srv-middleware', 'display_name': 'middleware-api', 'entity_type': 'service', 'health_status': 'healthy'},
            {'entity_id': 'srv-backend', 'display_name': 'backend-core', 'entity_type': 'service', 'health_status': 'healthy'},
            {'entity_id': 'db-postgres', 'display_name': 'postgres-db', 'entity_type': 'database', 'health_status': 'healthy'},
            {'entity_id': 'cache-redis', 'display_name': 'redis-cache', 'entity_type': 'cache', 'health_status': 'healthy'},
            {'entity_id': 'msg-kafka', 'display_name': 'kafka-cluster', 'entity_type': 'queue', 'health_status': 'healthy'},
            {'entity_id': 'host-aws-01', 'display_name': 'aws-ec2-prod-01', 'entity_type': 'host', 'health_status': 'healthy'},
            {'entity_id': 'host-aws-02', 'display_name': 'aws-ec2-prod-02', 'entity_type': 'host', 'health_status': 'warning'},
        ]
        
        entities = {}
        for data in entities_data:
            entity = GrailEntity.objects.create(
                entity_id=data['entity_id'],
                display_name=data['display_name'],
                entity_type=data['entity_type'],
                health_status=data['health_status'],
                last_seen=timezone.now(),
                properties={'env': 'production', 'version': '1.2.0'}
            )
            entities[data['entity_id']] = entity
            
        # Create Relationships
        relationships_data = [
            ('srv-frontend', 'srv-middleware', 'calls'),
            ('srv-middleware', 'srv-backend', 'calls'),
            ('srv-backend', 'db-postgres', 'queries'),
            ('srv-backend', 'cache-redis', 'uses'),
            ('srv-middleware', 'msg-kafka', 'publishes'),
            ('srv-frontend', 'host-aws-01', 'runs_on'),
            ('srv-middleware', 'host-aws-01', 'runs_on'),
            ('srv-backend', 'host-aws-02', 'runs_on'),
        ]
        
        for source_id, target_id, rel_type in relationships_data:
            GrailRelationship.objects.get_or_create(
                source=entities[source_id],
                target=entities[target_id],
                relationship_type=rel_type
            )
            
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(entities)} entities and {len(relationships_data)} relationships'))
