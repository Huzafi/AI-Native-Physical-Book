"""
Performance monitoring and alerting for AI-Native Book backend
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
import json
import psutil
import os

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MetricType(Enum):
    RESPONSE_TIME = "response_time"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    DATABASE_CONNECTIONS = "database_connections"
    CACHE_HIT_RATE = "cache_hit_rate"
    AI_RESPONSE_TIME = "ai_response_time"
    SEARCH_RESPONSE_TIME = "search_response_time"

@dataclass
class PerformanceMetric:
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    tags: Optional[Dict[str, str]] = None

@dataclass
class Alert:
    name: str
    description: str
    severity: AlertSeverity
    timestamp: datetime
    value: float
    threshold: float
    metric_name: str

class PerformanceMonitor:
    """
    Monitors application performance and triggers alerts when thresholds are exceeded
    """
    def __init__(self, alert_callback: Optional[Callable[[Alert], None]] = None):
        self.metrics: List[PerformanceMetric] = []
        self.alerts: List[Alert] = []
        self.alert_thresholds = {
            MetricType.RESPONSE_TIME: {"high": 2.0, "critical": 5.0},  # seconds
            MetricType.ERROR_RATE: {"high": 0.05, "critical": 0.10},  # percentage
            MetricType.MEMORY_USAGE: {"high": 0.80, "critical": 0.90},  # percentage
            MetricType.CPU_USAGE: {"high": 0.80, "critical": 0.90},  # percentage
            MetricType.CACHE_HIT_RATE: {"high": 0.70, "critical": 0.50},  # percentage
            MetricType.AI_RESPONSE_TIME: {"high": 3.0, "critical": 8.0},  # seconds
            MetricType.SEARCH_RESPONSE_TIME: {"high": 1.5, "critical": 4.0},  # seconds
        }
        self.alert_callback = alert_callback or self.default_alert_callback
        self.is_monitoring = False
        self.monitoring_task = None

    def record_metric(self, name: str, value: float, metric_type: MetricType, tags: Optional[Dict[str, str]] = None):
        """Record a performance metric"""
        metric = PerformanceMetric(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.now(),
            tags=tags
        )
        self.metrics.append(metric)

        # Check if this metric triggers any alerts
        self._check_thresholds(metric)

    def _check_thresholds(self, metric: PerformanceMetric):
        """Check if a metric exceeds any thresholds"""
        if metric.metric_type in self.alert_thresholds:
            thresholds = self.alert_thresholds[metric.metric_type]

            # Check high threshold
            if "high" in thresholds and metric.value > thresholds["high"]:
                alert = Alert(
                    name=f"{metric.metric_type.value}_high",
                    description=f"{metric.metric_type.value} exceeded high threshold",
                    severity=AlertSeverity.HIGH,
                    timestamp=metric.timestamp,
                    value=metric.value,
                    threshold=thresholds["high"],
                    metric_name=metric.name
                )
                self._trigger_alert(alert)

            # Check critical threshold
            if "critical" in thresholds and metric.value > thresholds["critical"]:
                alert = Alert(
                    name=f"{metric.metric_type.value}_critical",
                    description=f"{metric.metric_type.value} exceeded critical threshold",
                    severity=AlertSeverity.CRITICAL,
                    timestamp=metric.timestamp,
                    value=metric.value,
                    threshold=thresholds["critical"],
                    metric_name=metric.name
                )
                self._trigger_alert(alert)

    def _trigger_alert(self, alert: Alert):
        """Trigger an alert"""
        self.alerts.append(alert)
        logger.warning(f"Performance Alert: {alert.name} - {alert.description} (Value: {alert.value}, Threshold: {alert.threshold})")

        # Call the alert callback in a separate thread to avoid blocking
        Thread(target=self.alert_callback, args=(alert,), daemon=True).start()

    def default_alert_callback(self, alert: Alert):
        """Default alert callback - logs the alert"""
        logger.error(f"ALERT: {alert.severity.value.upper()} - {alert.description}")
        logger.error(f"  Metric: {alert.metric_name}")
        logger.error(f"  Value: {alert.value}")
        logger.error(f"  Threshold: {alert.threshold}")
        logger.error(f"  Time: {alert.timestamp}")

    def get_metrics_summary(self, time_window_minutes: int = 5) -> Dict:
        """Get summary of metrics for the specified time window"""
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
        recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]

        summary = {
            "time_window_minutes": time_window_minutes,
            "total_metrics": len(recent_metrics),
            "by_type": {},
            "alerts_triggered": len([a for a in self.alerts if a.timestamp >= cutoff_time])
        }

        # Group metrics by type and calculate statistics
        for metric_type in MetricType:
            type_metrics = [m for m in recent_metrics if m.metric_type == metric_type]
            if type_metrics:
                values = [m.value for m in type_metrics]
                summary["by_type"][metric_type.value] = {
                    "count": len(values),
                    "avg": sum(values) / len(values) if values else 0,
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0,
                    "p95": self._calculate_percentile(values, 95) if values else 0,
                    "p99": self._calculate_percentile(values, 99) if values else 0
                }

        return summary

    def _calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of a list of values"""
        if not values:
            return 0

        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)
        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def start_monitoring(self, interval_seconds: int = 30):
        """Start continuous monitoring"""
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.monitoring_task = Thread(target=self._monitoring_loop, args=(interval_seconds,), daemon=True)
        self.monitoring_task.start()
        logger.info(f"Performance monitoring started with {interval_seconds}s interval")

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.join(timeout=1)
        logger.info("Performance monitoring stopped")

    def _monitoring_loop(self, interval_seconds: int):
        """Continuous monitoring loop"""
        while self.is_monitoring:
            try:
                # Record system metrics
                self._record_system_metrics()

                # Clean old metrics (keep last hour)
                cutoff_time = datetime.now() - timedelta(hours=1)
                self.metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]

                time.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval_seconds)  # Continue monitoring even if there's an error

    def _record_system_metrics(self):
        """Record system-level metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.record_metric(
            name="system_cpu_usage",
            value=cpu_percent / 100.0,
            metric_type=MetricType.CPU_USAGE
        )

        # Memory usage
        memory_percent = psutil.virtual_memory().percent
        self.record_metric(
            name="system_memory_usage",
            value=memory_percent / 100.0,
            metric_type=MetricType.MEMORY_USAGE
        )

        # Process-specific memory usage
        process = psutil.Process(os.getpid())
        process_memory = process.memory_percent()
        self.record_metric(
            name="process_memory_usage",
            value=process_memory / 100.0,
            metric_type=MetricType.MEMORY_USAGE,
            tags={"process": "backend"}
        )

    def get_active_alerts(self) -> List[Alert]:
        """Get currently active alerts (within last 15 minutes)"""
        cutoff_time = datetime.now() - timedelta(minutes=15)
        return [a for a in self.alerts if a.timestamp >= cutoff_time]

    def get_alert_history(self, hours: int = 24) -> List[Alert]:
        """Get alert history for the specified number of hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [a for a in self.alerts if a.timestamp >= cutoff_time]

    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# Context managers and decorators for easy monitoring
class MonitorResponseTime:
    """Context manager to monitor response time"""
    def __init__(self, name: str, metric_type: MetricType = MetricType.RESPONSE_TIME):
        self.name = name
        self.metric_type = metric_type
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            performance_monitor.record_metric(
                name=self.name,
                value=duration,
                metric_type=self.metric_type
            )

def monitor_performance(name: str, metric_type: MetricType = MetricType.RESPONSE_TIME):
    """Decorator to monitor performance of a function"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with MonitorResponseTime(name, metric_type):
                return func(*args, **kwargs)
        return wrapper
    return decorator

def record_error_rate(success: bool, name: str = "general"):
    """Record error rate"""
    error_rate = 0 if success else 1
    performance_monitor.record_metric(
        name=f"{name}_error_rate",
        value=error_rate,
        metric_type=MetricType.ERROR_RATE
    )

def record_cache_hit_rate(hit: bool, name: str = "general"):
    """Record cache hit rate"""
    hit_rate = 1.0 if hit else 0.0
    performance_monitor.record_metric(
        name=f"{name}_cache_hit_rate",
        value=hit_rate,
        metric_type=MetricType.CACHE_HIT_RATE
    )

def get_performance_dashboard_data():
    """Get data formatted for a performance dashboard"""
    summary = performance_monitor.get_metrics_summary(time_window_minutes=5)

    dashboard_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "system_metrics": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('.').percent,
            "process_count": len(psutil.pids())
        },
        "active_alerts": len(performance_monitor.get_active_alerts()),
        "total_alerts": len(performance_monitor.alerts)
    }

    return dashboard_data

# Initialize monitoring when module is loaded
performance_monitor.start_monitoring()