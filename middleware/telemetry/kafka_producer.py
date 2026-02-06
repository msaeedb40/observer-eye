"""
Kafka Producer for Observer-Eye Telemetry.
High-throughput telemetry ingestion via Kafka.
"""
import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import aiokafka for async Kafka support
try:
    from aiokafka import AIOKafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logger.warning("aiokafka not installed. Kafka producer will be disabled.")


class TelemetryKafkaProducer:
    """Async Kafka producer for telemetry data."""
    
    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None
        self.bootstrap_servers = os.getenv('KAFKA_BROKERS', 'kafka:9092')
        self.is_connected = False
    
    async def connect(self):
        """Connect to Kafka cluster."""
        if not KAFKA_AVAILABLE:
            logger.warning("Kafka not available, skipping connection")
            return
        
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                compression_type='gzip',
                acks='all',
                enable_idempotence=True
            )
            await self.producer.start()
            self.is_connected = True
            logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            self.is_connected = False
    
    async def disconnect(self):
        """Disconnect from Kafka cluster."""
        if self.producer:
            await self.producer.stop()
            self.is_connected = False
            logger.info("Disconnected from Kafka")
    
    async def send_metric(self, metric: dict):
        """Send a single metric to Kafka."""
        await self._send('telemetry-metrics', metric, metric.get('name'))
    
    async def send_metrics(self, metrics: list):
        """Send multiple metrics to Kafka."""
        for metric in metrics:
            await self.send_metric(metric)
    
    async def send_log(self, log_entry: dict):
        """Send a log entry to Kafka."""
        await self._send('telemetry-logs', log_entry, log_entry.get('source'))
    
    async def send_logs(self, logs: list):
        """Send multiple log entries to Kafka."""
        for log in logs:
            await self.send_log(log)
    
    async def send_trace(self, trace: dict):
        """Send a trace to Kafka."""
        await self._send('telemetry-traces', trace, trace.get('trace_id'))
    
    async def send_traces(self, traces: list):
        """Send multiple traces to Kafka."""
        for trace in traces:
            await self.send_trace(trace)
    
    async def send_event(self, event: dict):
        """Send an event to Kafka."""
        await self._send('telemetry-events', event, event.get('event_type'))
    
    async def send_events(self, events: list):
        """Send multiple events to Kafka."""
        for event in events:
            await self.send_event(event)
    
    async def _send(self, topic: str, value: dict, key: Optional[str] = None):
        """Internal method to send message to Kafka topic."""
        if not self.is_connected:
            logger.warning(f"Not connected to Kafka, falling back to direct processing")
            return False
        
        try:
            await self.producer.send_and_wait(topic, value=value, key=key)
            return True
        except Exception as e:
            logger.error(f"Failed to send message to {topic}: {e}")
            return False


# Singleton instance
_kafka_producer: Optional[TelemetryKafkaProducer] = None


async def get_kafka_producer() -> TelemetryKafkaProducer:
    """Get or create Kafka producer singleton."""
    global _kafka_producer
    if _kafka_producer is None:
        _kafka_producer = TelemetryKafkaProducer()
        await _kafka_producer.connect()
    return _kafka_producer


async def close_kafka_producer():
    """Close Kafka producer."""
    global _kafka_producer
    if _kafka_producer:
        await _kafka_producer.disconnect()
        _kafka_producer = None
