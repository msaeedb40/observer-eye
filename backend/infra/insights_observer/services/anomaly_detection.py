"""
Anomaly Detection Service for Observer-Eye Platform.

Implements statistical anomaly detection algorithms:
- Z-Score (Standard Deviation)
- IQR (Interquartile Range)
- Moving Average Deviation
- Threshold-based detection

Designed for real-time and batch processing of observability data.
"""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import statistics
from django.utils import timezone
from django.db.models import Avg, StdDev, Max, Min, Count

logger = logging.getLogger(__name__)


class DetectionMethod(str, Enum):
    """Available anomaly detection methods."""
    ZSCORE = "zscore"
    IQR = "iqr"
    MOVING_AVERAGE = "moving_average"
    THRESHOLD = "threshold"
    RATE_CHANGE = "rate_change"


@dataclass
class AnomalyResult:
    """Result of anomaly detection analysis."""
    is_anomaly: bool
    metric_name: str
    source: str
    expected_value: float
    actual_value: float
    deviation_score: float
    detection_method: DetectionMethod
    confidence: float  # 0.0 to 1.0
    message: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = timezone.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'is_anomaly': self.is_anomaly,
            'metric_name': self.metric_name,
            'source': self.source,
            'expected_value': self.expected_value,
            'actual_value': self.actual_value,
            'deviation_score': self.deviation_score,
            'detection_method': self.detection_method.value,
            'confidence': self.confidence,
            'message': self.message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
        }


class DetectionAlgorithm(ABC):
    """Abstract base class for detection algorithms."""
    
    @abstractmethod
    def detect(
        self, 
        values: List[float], 
        current_value: float,
        config: Dict[str, Any]
    ) -> Tuple[bool, float, float, str]:
        """
        Detect if current value is an anomaly.
        
        Args:
            values: Historical values for baseline
            current_value: The current value to check
            config: Algorithm-specific configuration
            
        Returns:
            Tuple of (is_anomaly, expected_value, deviation_score, message)
        """
        raise NotImplementedError("Subclasses must implement detect()")


class ZScoreDetector(DetectionAlgorithm):
    """Z-Score based anomaly detection."""
    
    def detect(
        self, 
        values: List[float], 
        current_value: float,
        config: Dict[str, Any]
    ) -> Tuple[bool, float, float, str]:
        if len(values) < 2:
            return False, current_value, 0.0, "Insufficient data for Z-score"
        
        threshold = config.get('threshold', 3.0)  # Standard deviations
        
        mean = statistics.mean(values)
        std_dev = statistics.stdev(values)
        
        if std_dev == 0:
            return False, mean, 0.0, "Zero standard deviation"
        
        z_score = abs(current_value - mean) / std_dev
        is_anomaly = z_score > threshold
        
        message = f"Z-score: {z_score:.2f} (threshold: {threshold})"
        if is_anomaly:
            direction = "above" if current_value > mean else "below"
            message = f"Value is {z_score:.2f} std devs {direction} mean"
        
        return is_anomaly, mean, z_score, message


class IQRDetector(DetectionAlgorithm):
    """Interquartile Range based anomaly detection."""
    
    def detect(
        self, 
        values: List[float], 
        current_value: float,
        config: Dict[str, Any]
    ) -> Tuple[bool, float, float, str]:
        if len(values) < 4:
            return False, current_value, 0.0, "Insufficient data for IQR"
        
        multiplier = config.get('multiplier', 1.5)  # IQR multiplier
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        q1 = sorted_values[n // 4]
        q3 = sorted_values[3 * n // 4]
        iqr = q3 - q1
        
        lower_bound = q1 - (multiplier * iqr)
        upper_bound = q3 + (multiplier * iqr)
        median = statistics.median(values)
        
        is_anomaly = current_value < lower_bound or current_value > upper_bound
        
        if iqr > 0:
            deviation_score = abs(current_value - median) / iqr
        else:
            deviation_score = 0.0
        
        message = f"IQR bounds: [{lower_bound:.2f}, {upper_bound:.2f}]"
        if is_anomaly:
            if current_value < lower_bound:
                message = f"Value {current_value:.2f} below lower bound {lower_bound:.2f}"
            else:
                message = f"Value {current_value:.2f} above upper bound {upper_bound:.2f}"
        
        return is_anomaly, median, deviation_score, message


class MovingAverageDetector(DetectionAlgorithm):
    """Moving average deviation based anomaly detection."""
    
    def detect(
        self, 
        values: List[float], 
        current_value: float,
        config: Dict[str, Any]
    ) -> Tuple[bool, float, float, str]:
        window_size = config.get('window_size', 10)
        deviation_threshold = config.get('deviation_threshold', 0.3)  # 30% deviation
        
        if len(values) < window_size:
            window = values
        else:
            window = values[-window_size:]
        
        if not window:
            return False, current_value, 0.0, "No data for moving average"
        
        moving_avg = statistics.mean(window)
        
        if moving_avg == 0:
            deviation = abs(current_value) if current_value != 0 else 0.0
        else:
            deviation = abs(current_value - moving_avg) / abs(moving_avg)
        
        is_anomaly = deviation > deviation_threshold
        
        message = f"Moving avg: {moving_avg:.2f}, deviation: {deviation:.2%}"
        if is_anomaly:
            message = f"Value deviates {deviation:.2%} from moving average {moving_avg:.2f}"
        
        return is_anomaly, moving_avg, deviation, message


class ThresholdDetector(DetectionAlgorithm):
    """Simple threshold-based anomaly detection."""
    
    def detect(
        self, 
        values: List[float], 
        current_value: float,
        config: Dict[str, Any]
    ) -> Tuple[bool, float, float, str]:
        min_threshold = config.get('min_threshold')
        max_threshold = config.get('max_threshold')
        
        expected = statistics.mean(values) if values else current_value
        is_anomaly = False
        deviation_score = 0.0
        messages = []
        
        if min_threshold is not None and current_value < min_threshold:
            is_anomaly = True
            deviation_score = abs(current_value - min_threshold)
            messages.append(f"Below min threshold {min_threshold}")
        
        if max_threshold is not None and current_value > max_threshold:
            is_anomaly = True
            deviation_score = abs(current_value - max_threshold)
            messages.append(f"Above max threshold {max_threshold}")
        
        message = "; ".join(messages) if messages else "Within thresholds"
        
        return is_anomaly, expected, deviation_score, message


class RateChangeDetector(DetectionAlgorithm):
    """Rate of change based anomaly detection."""
    
    def detect(
        self, 
        values: List[float], 
        current_value: float,
        config: Dict[str, Any]
    ) -> Tuple[bool, float, float, str]:
        rate_threshold = config.get('rate_threshold', 0.5)  # 50% change rate
        
        if not values:
            return False, current_value, 0.0, "No previous values"
        
        previous_value = values[-1]
        
        if previous_value == 0:
            if current_value == 0:
                rate_change = 0.0
            else:
                rate_change = float('inf')
        else:
            rate_change = abs(current_value - previous_value) / abs(previous_value)
        
        is_anomaly = rate_change > rate_threshold
        
        message = f"Rate of change: {rate_change:.2%}"
        if is_anomaly:
            direction = "increased" if current_value > previous_value else "decreased"
            message = f"Value {direction} by {rate_change:.2%}"
        
        return is_anomaly, previous_value, rate_change, message


# Detector registry
DETECTORS = {
    DetectionMethod.ZSCORE: ZScoreDetector(),
    DetectionMethod.IQR: IQRDetector(),
    DetectionMethod.MOVING_AVERAGE: MovingAverageDetector(),
    DetectionMethod.THRESHOLD: ThresholdDetector(),
    DetectionMethod.RATE_CHANGE: RateChangeDetector(),
}


class AnomalyDetectionService:
    """
    Main anomaly detection service.
    
    Usage:
        service = AnomalyDetectionService()
        
        # Single metric analysis
        result = service.analyze_metric('cpu_usage', 'app-01', 95.5)
        
        # Batch analysis
        results = service.analyze_all_metrics()
    """
    
    def __init__(self, default_method: DetectionMethod = DetectionMethod.ZSCORE):
        self.default_method = default_method
        self.detectors = DETECTORS
        self.lookback_period = timedelta(hours=24)  # Default lookback for baseline
    
    def analyze_metric(
        self,
        metric_name: str,
        source: str,
        current_value: float,
        method: DetectionMethod = None,
        config: Dict[str, Any] = None,
        save_result: bool = True,
    ) -> AnomalyResult:
        """
        Analyze a single metric for anomalies.
        
        Args:
            metric_name: Name of the metric
            source: Source/host identifier
            current_value: Current metric value
            method: Detection method to use
            config: Algorithm configuration
            save_result: Whether to save anomaly to database
            
        Returns:
            AnomalyResult with detection details
        """
        from core.models import Metric
        
        method = method or self.default_method
        config = config or {}
        
        # Get historical values for baseline
        cutoff = timezone.now() - self.lookback_period
        historical = Metric.objects.filter(
            name=metric_name,
            source=source,
            timestamp__gte=cutoff,
        ).order_by('timestamp').values_list('value', flat=True)
        
        values = list(historical)
        
        # Run detection
        detector = self.detectors.get(method)
        if not detector:
            return AnomalyResult(
                is_anomaly=False,
                metric_name=metric_name,
                source=source,
                expected_value=current_value,
                actual_value=current_value,
                deviation_score=0.0,
                detection_method=method,
                confidence=0.0,
                message=f"Unknown detection method: {method}",
            )
        
        is_anomaly, expected, deviation, message = detector.detect(values, current_value, config)
        
        # Calculate confidence based on data quality
        confidence = self._calculate_confidence(values, deviation)
        
        result = AnomalyResult(
            is_anomaly=is_anomaly,
            metric_name=metric_name,
            source=source,
            expected_value=expected,
            actual_value=current_value,
            deviation_score=deviation,
            detection_method=method,
            confidence=confidence,
            message=message,
        )
        
        # Save to database if anomaly detected
        if save_result and is_anomaly:
            self._save_anomaly(result)
            self._create_insight(result)
        
        return result
    
    def _calculate_confidence(self, values: List[float], deviation: float) -> float:
        """Calculate confidence score based on data quality."""
        if not values:
            return 0.0
        
        # More data points = higher confidence
        data_confidence = min(len(values) / 100, 1.0)
        
        # Higher deviation = higher confidence in anomaly
        deviation_confidence = min(deviation / 5, 1.0) if deviation else 0.5
        
        return (data_confidence * 0.6 + deviation_confidence * 0.4)
    
    def _save_anomaly(self, result: AnomalyResult):
        """Save anomaly detection result to database."""
        from .models import AnomalyDetection
        
        AnomalyDetection.objects.create(
            metric_name=result.metric_name,
            source=result.source,
            expected_value=result.expected_value,
            actual_value=result.actual_value,
            deviation_score=result.deviation_score,
        )
    
    def _create_insight(self, result: AnomalyResult):
        """Create an insight from anomaly detection."""
        from .models import Insight
        
        Insight.objects.create(
            title=f"Anomaly detected: {result.metric_name}",
            description=result.message,
            insight_type='anomaly',
            severity='warning' if result.deviation_score < 3 else 'critical',
            data_source=f"{result.metric_name}@{result.source}",
            related_entities=[result.source],
            evidence={
                'expected_value': result.expected_value,
                'actual_value': result.actual_value,
                'deviation_score': result.deviation_score,
                'detection_method': result.detection_method.value,
                'confidence': result.confidence,
            },
            recommendations=[
                f"Investigate {result.metric_name} on {result.source}",
                f"Check for related events around {result.timestamp}",
            ],
        )
    
    def analyze_all_metrics(
        self,
        method: DetectionMethod = None,
        config: Dict[str, Any] = None,
        limit: int = 100,
    ) -> List[AnomalyResult]:
        """
        Analyze recent metrics across all sources for anomalies.
        
        Returns:
            List of AnomalyResult for detected anomalies
        """
        from core.models import Metric
        
        results = []
        
        # Get distinct metric/source combinations with recent data
        recent_cutoff = timezone.now() - timedelta(minutes=5)
        recent_metrics = Metric.objects.filter(
            timestamp__gte=recent_cutoff
        ).values('name', 'source').distinct()[:limit]
        
        for entry in recent_metrics:
            # Get the latest value for this metric/source
            latest = Metric.objects.filter(
                name=entry['name'],
                source=entry['source'],
            ).order_by('-timestamp').first()
            
            if latest:
                result = self.analyze_metric(
                    metric_name=entry['name'],
                    source=entry['source'],
                    current_value=latest.value,
                    method=method,
                    config=config,
                )
                
                if result.is_anomaly:
                    results.append(result)
        
        return results


# Convenience functions
def detect_anomaly(
    metric_name: str,
    source: str,
    current_value: float,
    method: str = 'zscore',
    **config
) -> Dict[str, Any]:
    """
    Convenience function for anomaly detection.
    
    Args:
        metric_name: Name of the metric
        source: Source identifier
        current_value: Current value to check
        method: Detection method ('zscore', 'iqr', 'moving_average', 'threshold')
        **config: Additional configuration for the detection method
        
    Returns:
        Dict with detection results
    """
    service = AnomalyDetectionService()
    detection_method = DetectionMethod(method)
    result = service.analyze_metric(
        metric_name=metric_name,
        source=source,
        current_value=current_value,
        method=detection_method,
        config=config,
    )
    return result.to_dict()
