"""
PromQL-compatible Query Engine for Observer-Eye.
Translates PromQL-like queries into backend lookups and perform aggregations.
"""
import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
import httpx
import os

logger = logging.getLogger(__name__)

class PromQLEngine:
    """
    Simplified PromQL engine for Observer-Eye.
    Supports:
    - Metric selection: metric_name{label="value"}
    - Aggregations: sum, avg, min, max, count
    - Functions: rate, irate, delta
    - Range queries and instant queries
    """
    
    AGGREGATION_FUNCTIONS = ['sum', 'avg', 'min', 'max', 'count']
    TRANSFORMATION_FUNCTIONS = ['rate', 'irate', 'delta', 'increase']
    
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or os.getenv('BACKEND_URL', 'http://localhost:8000')
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parses a simplified PromQL query.
        Example: sum(rate(cpu_usage{host="server-1"}[5m]))
        """
        # Very basic regex-based parsing for demonstration
        # In a real scenario, use a proper parser (e.g., ply or a simplified PromQL parser)
        
        # 1. Check for aggregation
        agg_match = re.match(r'^(\w+)\((.*)\)$', query)
        if agg_match:
            func = agg_match.group(1)
            inner = agg_match.group(2)
            if func in self.AGGREGATION_FUNCTIONS:
                return {
                    'type': 'aggregation',
                    'function': func,
                    'query': self.parse_query(inner)
                }
            elif func in self.TRANSFORMATION_FUNCTIONS:
                return {
                    'type': 'transformation',
                    'function': func,
                    'query': self.parse_query(inner)
                }

        # 2. Check for range selector
        range_match = re.match(r'^(.*)\[(\d+)([smhd])\]$', query)
        if range_match:
            inner = range_match.group(1)
            duration = int(range_match.group(2))
            unit = range_match.group(3)
            return {
                'type': 'range_selection',
                'duration_seconds': self._to_seconds(duration, unit),
                'query': self.parse_query(inner)
            }

        # 3. Metric selection
        metric_match = re.match(r'^([\w_]+)({.*})?$', query)
        if metric_match:
            metric_name = metric_match.group(1)
            labels_str = metric_match.group(2) or "{}"
            labels = self._parse_labels(labels_str)
            return {
                'type': 'metric_selection',
                'metric_name': metric_name,
                'labels': labels
            }
        
        return {'type': 'unknown', 'query': query}

    async def execute_instant(self, query: str, time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Executes an instant query at a specific point in time."""
        parsed = self.parse_query(query)
        time = time or datetime.utcnow()
        
        logger.info(f"Executing instant query: {query} at {time}")
        
        # If it's a simple metric selection, fetch from backend
        if parsed['type'] == 'metric_selection':
            return await self._fetch_metrics(
                parsed['metric_name'], 
                parsed['labels'], 
                start=time - timedelta(minutes=1),
                end=time,
                limit=1
            )
        
        # For more complex queries, this would recursively evaluate the AST
        # Simple placeholder for aggregation
        if parsed['type'] == 'aggregation':
            data = await self.execute_instant(parsed['query']['query'], time)
            return self._apply_aggregation(parsed['function'], data)

        return []

    async def execute_range(self, query: str, start: datetime, end: datetime, step: str) -> List[Dict[str, Any]]:
        """Executes a range query over a time window."""
        parsed = self.parse_query(query)
        logger.info(f"Executing range query: {query} from {start} to {end} step {step}")
        
        if parsed['type'] == 'metric_selection':
            return await self._fetch_metrics(
                parsed['metric_name'],
                parsed['labels'],
                start=start,
                end=end
            )
        
        # Placeholder for more complex logic
        return []

    async def _fetch_metrics(self, name: str, labels: Dict[str, str], start: datetime, end: datetime, limit: int = None) -> List[Dict[str, Any]]:
        """Fetches raw metrics from the backend."""
        params = {
            'name': name,
            'timestamp__gte': start.isoformat(),
            'timestamp__lte': end.isoformat(),
        }
        # Add labels to params
        for k, v in labels.items():
            params[f'labels__{k}'] = v
            
        if limit:
            params['limit'] = limit

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.backend_url}/api/v1/core/metrics/",
                    params=params
                )
                if response.status_code == 200:
                    return response.json()
                logger.error(f"Backend returned {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"Error fetching metrics: {e}")
            
        return []

    def _parse_labels(self, labels_str: str) -> Dict[str, str]:
        """Parses PromQL label string like {host="server-1", app="web"}."""
        labels = {}
        # Remove braces
        content = labels_str.strip('{}')
        if not content:
            return labels
            
        pairs = content.split(',')
        for pair in pairs:
            if '=' in pair:
                k, v = pair.split('=')
                labels[k.strip()] = v.strip(' "')
        return labels

    def _to_seconds(self, duration: int, unit: str) -> int:
        """Converts duration units to seconds."""
        units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        return duration * units.get(unit, 1)

    def _apply_aggregation(self, func: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Applies aggregation functions to data."""
        if not data:
            return []
            
        values = [d.get('value', 0) for d in data]
        
        result = {'type': 'scalar', 'function': func, 'timestamp': datetime.utcnow().isoformat()}
        
        if func == 'sum':
            result['value'] = sum(values)
        elif func == 'avg':
            result['value'] = sum(values) / len(values) if values else 0
        elif func == 'min':
            result['value'] = min(values) if values else 0
        elif func == 'max':
            result['value'] = max(values) if values else 0
        elif func == 'count':
            result['value'] = len(values)
            
        return [result]
