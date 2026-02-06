"""
Kafka Consumer for Observer-Eye Telemetry.
Consumes telemetry data from Kafka and delegates to Celery for processing.
"""
import os
import json
import asyncio
import logging
from aiokafka import AIOKafkaConsumer
from telemetry.celery_tasks import (
    process_metrics_batch,
    process_logs_batch,
    process_traces_batch
)

logger = logging.getLogger("telemetry_kafka_consumer")

# Configuration
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'kafka:9092')
TOPICS = ['telemetry-metrics', 'telemetry-logs', 'telemetry-traces', 'telemetry-events']
GROUP_ID = "telemetry-processor-group"

async def consume():
    """Main consumption loop."""
    consumer = AIOKafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_BROKERS,
        group_id=GROUP_ID,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    
    logger.info(f"Starting Kafka consumer on {KAFKA_BROKERS} for topics {TOPICS}")
    
    await consumer.start()
    try:
        async for msg in consumer:
            topic = msg.topic
            data = msg.value
            
            # Ensure data is a list for batch processing logic
            if not isinstance(data, list):
                data = [data]
                
            logger.info(f"Received batch from {topic} (size: {len(data)})")
            
            try:
                if topic == 'telemetry-metrics':
                    process_metrics_batch.delay(data)
                elif topic == 'telemetry-logs':
                    process_logs_batch.delay(data)
                elif topic == 'telemetry-traces':
                    process_traces_batch.delay(data)
                elif topic == 'telemetry-events':
                    # Events could be metrics or specialized alerts
                    process_metrics_batch.delay(data)
            except Exception as e:
                logger.error(f"Failed to delegate task for {topic}: {e}")
                
    except Exception as e:
        logger.error(f"Consumer error: {e}")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(consume())
