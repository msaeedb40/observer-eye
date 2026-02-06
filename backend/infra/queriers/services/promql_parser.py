"""
PromQL-like Query Parser Service for Observer-Eye Platform.

Supports a simplified PromQL-like syntax for querying observability data.

Syntax Examples:
  - metrics{name="cpu_usage", source="app-01"}
  - logs{level="error", source~="web-.*"}
  - traces{service_name="auth-service", status="error"}
  - avg(metrics{name="memory_usage"})[5m]
  - rate(metrics{name="requests_total"})[1m]

Operators:
  - = : exact match
  - != : not equal
  - =~ : regex match
  - !~ : regex not match
  - > : greater than (numeric)
  - < : less than (numeric)
  - >= : greater or equal
  - <= : less or equal
"""
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from django.db.models import Q, Avg, Count, Max, Min, Sum
from django.utils import timezone


class DataType(Enum):
    METRICS = "metrics"
    LOGS = "logs"
    TRACES = "traces"
    EVENTS = "events"
    SPANS = "spans"


class Operator(Enum):
    EQ = "="
    NE = "!="
    REGEX = "=~"
    NOT_REGEX = "!~"
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="


class AggregateFunction(Enum):
    AVG = "avg"
    SUM = "sum"
    COUNT = "count"
    MAX = "max"
    MIN = "min"
    RATE = "rate"
    INCREASE = "increase"


@dataclass
class LabelMatcher:
    """A single label matcher (e.g., name="cpu_usage")."""
    key: str
    operator: Operator
    value: str


@dataclass
class QueryExpression:
    """Parsed query expression."""
    data_type: DataType
    matchers: List[LabelMatcher]
    aggregate_fn: Optional[AggregateFunction] = None
    time_range: Optional[str] = None  # e.g., "5m", "1h", "24h"
    limit: int = 100


class QueryParseError(Exception):
    """Raised when query parsing fails."""
    pass


class PromQLParser:
    """
    Parser for PromQL-like query syntax.
    
    Grammar (simplified):
      query := [aggregate_fn "(" ] data_type "{" labels "}" [ ")" ] [ "[" duration "]" ]
      aggregate_fn := "avg" | "sum" | "count" | "max" | "min" | "rate" | "increase"
      data_type := "metrics" | "logs" | "traces" | "events" | "spans"
      labels := label ("," label)*
      label := key operator value
      operator := "=" | "!=" | "=~" | "!~" | ">" | "<" | ">=" | "<="
      duration := number ("s" | "m" | "h" | "d")
    """
    
    # Regex patterns
    AGGREGATE_PATTERN = re.compile(r'^(\w+)\s*\(\s*(.+)\s*\)\s*(\[\d+[smhd]\])?$')
    BASIC_PATTERN = re.compile(r'^(\w+)\s*\{([^}]*)\}\s*(\[\d+[smhd]\])?$')
    LABEL_PATTERN = re.compile(r'(\w+)\s*(=~|!~|!=|>=|<=|=|>|<)\s*"([^"]*)"')
    DURATION_PATTERN = re.compile(r'\[(\d+)([smhd])\]')
    
    @classmethod
    def parse(cls, query: str) -> QueryExpression:
        """Parse a PromQL-like query string into a QueryExpression."""
        query = query.strip()
        
        aggregate_fn = None
        time_range = None
        
        # Check for aggregate function wrapper
        agg_match = cls.AGGREGATE_PATTERN.match(query)
        if agg_match:
            fn_name = agg_match.group(1).lower()
            try:
                aggregate_fn = AggregateFunction(fn_name)
            except ValueError:
                raise QueryParseError(f"Unknown aggregate function: {fn_name}")
            query = agg_match.group(2).strip()
            if agg_match.group(3):
                time_range = agg_match.group(3).strip('[]')
        
        # Parse basic pattern: data_type{labels}[duration]
        basic_match = cls.BASIC_PATTERN.match(query)
        if not basic_match:
            # Handle simple query like "up" or "cpu_usage" as metric name lookup
            simple_name = re.match(r'^(\w+)$', query)
            if simple_name:
                return QueryExpression(
                    data_type=DataType.METRICS,
                    matchers=[LabelMatcher(key='name', operator=Operator.EQ, value=simple_name.group(1))],
                    aggregate_fn=aggregate_fn,
                    time_range=time_range
                )
            raise QueryParseError(f"Invalid query syntax: {query}")
        
        data_type_str = basic_match.group(1).lower()
        labels_str = basic_match.group(2)
        duration_str = basic_match.group(3)
        
        # Parse data type
        try:
            data_type = DataType(data_type_str)
        except ValueError:
            raise QueryParseError(f"Unknown data type: {data_type_str}")
        
        # Parse labels
        matchers = []
        if labels_str.strip():
            for match in cls.LABEL_PATTERN.finditer(labels_str):
                key = match.group(1)
                op_str = match.group(2)
                value = match.group(3)
                
                op_map = {
                    "=": Operator.EQ,
                    "!=": Operator.NE,
                    "=~": Operator.REGEX,
                    "!~": Operator.NOT_REGEX,
                    ">": Operator.GT,
                    "<": Operator.LT,
                    ">=": Operator.GTE,
                    "<=": Operator.LTE,
                }
                matchers.append(LabelMatcher(key=key, operator=op_map[op_str], value=value))
        
        # Parse duration if present
        if duration_str and not time_range:
            time_range = duration_str.strip('[]')
        
        return QueryExpression(
            data_type=data_type,
            matchers=matchers,
            aggregate_fn=aggregate_fn,
            time_range=time_range
        )
    
    @classmethod
    def duration_to_timedelta(cls, duration: str) -> timedelta:
        """Convert duration string (e.g., '5m', '1h') to timedelta."""
        match = re.match(r'^(\d+)([smhd])$', duration)
        if not match:
            raise QueryParseError(f"Invalid duration format: {duration}")
        
        value = int(match.group(1))
        unit = match.group(2)
        
        unit_map = {
            's': timedelta(seconds=value),
            'm': timedelta(minutes=value),
            'h': timedelta(hours=value),
            'd': timedelta(days=value),
        }
        return unit_map[unit]


class QueryExecutor:
    """Executes parsed queries against Django models."""
    
    def __init__(self):
        self.model_map = {}
        self._init_models()
    
    def _init_models(self):
        """Initialize model mapping."""
        try:
            from core.models import Metric, Event, LogEntry, Trace, Span
            self.model_map = {
                DataType.METRICS: Metric,
                DataType.EVENTS: Event,
                DataType.LOGS: LogEntry,
                DataType.TRACES: Trace,
                DataType.SPANS: Span,
            }
        except ImportError as e:
            logger.warning(f"Could not initialize models for QueryExecutor: {e}. Some data types may be unavailable.")
    
    def execute(self, expr: QueryExpression) -> Dict[str, Any]:
        """Execute a parsed query expression."""
        if not self.model_map:
            self._init_models()
        
        model = self.model_map.get(expr.data_type)
        if not model:
            raise QueryParseError(f"Model not found for data type: {expr.data_type}")
        
        # Build Django queryset
        qs = model.objects.all()
        
        # Apply time range filter
        if expr.time_range:
            delta = PromQLParser.duration_to_timedelta(expr.time_range)
            time_field = 'timestamp' if hasattr(model, 'timestamp') else 'start_time'
            cutoff = timezone.now() - delta
            qs = qs.filter(**{f'{time_field}__gte': cutoff})
        
        # Apply label matchers
        for matcher in expr.matchers:
            qs = self._apply_matcher(qs, matcher)
        
        # Apply aggregation or return raw results
        if expr.aggregate_fn:
            return self._apply_aggregate(qs, expr)
        else:
            return self._serialize_results(qs.order_by('-created_at')[:expr.limit], expr.data_type)
    
    def _apply_matcher(self, qs, matcher: LabelMatcher):
        """Apply a single label matcher to queryset."""
        key = matcher.key
        value = matcher.value
        
        if matcher.operator == Operator.EQ:
            return qs.filter(**{key: value})
        elif matcher.operator == Operator.NE:
            return qs.exclude(**{key: value})
        elif matcher.operator == Operator.REGEX:
            return qs.filter(**{f'{key}__regex': value})
        elif matcher.operator == Operator.NOT_REGEX:
            return qs.exclude(**{f'{key}__regex': value})
        elif matcher.operator == Operator.GT:
            return qs.filter(**{f'{key}__gt': float(value)})
        elif matcher.operator == Operator.LT:
            return qs.filter(**{f'{key}__lt': float(value)})
        elif matcher.operator == Operator.GTE:
            return qs.filter(**{f'{key}__gte': float(value)})
        elif matcher.operator == Operator.LTE:
            return qs.filter(**{f'{key}__lte': float(value)})
        
        return qs
    
    def _apply_aggregate(self, qs, expr: QueryExpression) -> Dict[str, Any]:
        """Apply aggregate function to queryset."""
        agg_map = {
            AggregateFunction.AVG: Avg,
            AggregateFunction.SUM: Sum,
            AggregateFunction.COUNT: Count,
            AggregateFunction.MAX: Max,
            AggregateFunction.MIN: Min,
        }
        
        if expr.aggregate_fn == AggregateFunction.COUNT:
            return {
                "aggregate": expr.aggregate_fn.value,
                "value": qs.count(),
                "time_range": expr.time_range,
            }
        
        if expr.aggregate_fn == AggregateFunction.RATE:
            # Rate = count / time_range_seconds
            count = qs.count()
            if expr.time_range:
                delta = PromQLParser.duration_to_timedelta(expr.time_range)
                rate = count / delta.total_seconds()
            else:
                rate = count
            return {
                "aggregate": "rate",
                "value": rate,
                "time_range": expr.time_range,
            }
        
        # For numeric aggregates on metrics
        if expr.data_type == DataType.METRICS:
            agg_fn = agg_map.get(expr.aggregate_fn)
            if agg_fn:
                result = qs.aggregate(result=agg_fn('value'))
                return {
                    "aggregate": expr.aggregate_fn.value,
                    "value": result.get('result'),
                    "time_range": expr.time_range,
                }
        
        return {"aggregate": expr.aggregate_fn.value, "value": None, "error": "Aggregate not applicable"}
    
    def _serialize_results(self, queryset, data_type: DataType) -> Dict[str, Any]:
        """Serialize queryset results based on data type."""
        results = []
        
        for obj in queryset:
            if data_type == DataType.METRICS:
                results.append({
                    "id": str(obj.id),
                    "timestamp": obj.timestamp.isoformat() if obj.timestamp else None,
                    "name": obj.name,
                    "value": obj.value,
                    "unit": obj.unit,
                    "source": obj.source,
                    "labels": obj.labels,
                })
            elif data_type == DataType.LOGS:
                results.append({
                    "id": str(obj.id),
                    "timestamp": obj.timestamp.isoformat() if obj.timestamp else None,
                    "level": obj.level,
                    "message": obj.message,
                    "source": obj.source,
                    "trace_id": obj.trace_id,
                })
            elif data_type == DataType.EVENTS:
                results.append({
                    "id": str(obj.id),
                    "timestamp": obj.timestamp.isoformat() if obj.timestamp else None,
                    "name": obj.name,
                    "event_type": obj.event_type,
                    "severity": obj.severity,
                    "source": obj.source,
                })
            elif data_type == DataType.TRACES:
                results.append({
                    "id": str(obj.id),
                    "trace_id": obj.trace_id,
                    "name": obj.name,
                    "service_name": obj.service_name,
                    "duration_ms": obj.duration_ms,
                    "status": obj.status,
                })
            elif data_type == DataType.SPANS:
                results.append({
                    "id": str(obj.id),
                    "span_id": obj.span_id,
                    "trace_id": str(obj.trace_id),
                    "name": obj.name,
                    "duration_ms": obj.duration_ms,
                    "status": obj.status,
                })
        
        return {
            "data_type": data_type.value,
            "count": len(results),
            "results": results,
        }


def execute_query(query_string: str, limit: int = 100) -> Dict[str, Any]:
    """
    Convenience function to parse and execute a query.
    
    Args:
        query_string: PromQL-like query string
        limit: Maximum number of results
    
    Returns:
        Dict with query results or error
    
    Example:
        >>> execute_query('metrics{name="cpu_usage", source="app-01"}')
        >>> execute_query('avg(metrics{name="memory_usage"})[5m]')
        >>> execute_query('logs{level="error"}')
    """
    try:
        expr = PromQLParser.parse(query_string)
        expr.limit = limit
        executor = QueryExecutor()
        return {"status": "success", **executor.execute(expr)}
    except QueryParseError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": f"Execution error: {str(e)}"}
