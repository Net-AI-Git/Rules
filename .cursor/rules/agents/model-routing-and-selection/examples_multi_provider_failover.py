"""
Multi-Provider Failover Examples

This file demonstrates multi-provider failover strategies for High Availability.
Reference this example from RULE.mdc using @examples_multi_provider_failover.py syntax.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import deque
import asyncio


# ============================================================================
# Provider Health Status
# ============================================================================

class ProviderHealthStatus(Enum):
    """
    Provider health status levels.
    
    This demonstrates health status classification:
    - Healthy: Provider is operational
    - Degraded: Provider has issues but still functional
    - Unhealthy: Provider is failing and should be avoided
    """
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class ProviderHealthMetrics:
    """
    Provider health metrics.
    
    This demonstrates health tracking:
    - Success rate
    - Average latency
    - Error rate
    - Last check time
    """
    provider_id: str
    success_rate: float = 1.0
    avg_latency: float = 0.0
    error_rate: float = 0.0
    last_check: Optional[datetime] = None
    consecutive_failures: int = 0
    total_requests: int = 0
    total_errors: int = 0


@dataclass
class ProviderConfig:
    """
    Provider configuration.
    
    This demonstrates provider setup:
    - Provider ID and name
    - Priority in failover chain
    - API endpoint and credentials
    - Health check configuration
    """
    provider_id: str
    provider_name: str
    priority: int  # Lower number = higher priority
    api_endpoint: str
    api_key: str
    health_check_interval: int = 30  # seconds
    latency_threshold: float = 5.0  # seconds
    error_rate_threshold: float = 0.1  # 10%
    max_consecutive_failures: int = 3


# ============================================================================
# Provider Health Monitor
# ============================================================================

class ProviderHealthMonitor:
    """
    Monitor provider health status.
    
    This demonstrates health monitoring patterns:
    - Periodic health checks
    - Request-based health tracking
    - Health status calculation
    - Automatic health recovery detection
    """
    
    def __init__(self, providers: List[ProviderConfig]):
        """
        Initialize health monitor.
        
        Args:
            providers: List of provider configurations
        """
        self.providers = {p.provider_id: p for p in providers}
        self.health_metrics: Dict[str, ProviderHealthMetrics] = {
            p.provider_id: ProviderHealthMetrics(provider_id=p.provider_id)
            for p in providers
        }
        self.health_status: Dict[str, ProviderHealthStatus] = {
            p.provider_id: ProviderHealthStatus.HEALTHY
            for p in providers
        }
        self.request_history: Dict[str, deque] = {
            p.provider_id: deque(maxlen=100)
            for p in providers
        }
    
    async def check_provider_health(
        self,
        provider_id: str
    ) -> ProviderHealthStatus:
        """
        Check provider health.
        
        Args:
            provider_id: Provider identifier
            
        Returns:
            ProviderHealthStatus
        """
        if provider_id not in self.providers:
            return ProviderHealthStatus.UNHEALTHY
        
        config = self.providers[provider_id]
        metrics = self.health_metrics[provider_id]
        
        # Perform health check
        is_healthy = await self._perform_health_check(config)
        
        # Update metrics
        metrics.last_check = datetime.now()
        metrics.total_requests += 1
        
        if not is_healthy:
            metrics.total_errors += 1
            metrics.consecutive_failures += 1
        else:
            metrics.consecutive_failures = 0
        
        # Calculate success rate
        if metrics.total_requests > 0:
            metrics.success_rate = 1.0 - (metrics.total_errors / metrics.total_requests)
            metrics.error_rate = metrics.total_errors / metrics.total_requests
        
        # Determine health status
        status = self._calculate_health_status(config, metrics)
        self.health_status[provider_id] = status
        
        return status
    
    async def _perform_health_check(
        self,
        config: ProviderConfig
    ) -> bool:
        """
        Perform actual health check.
        
        Args:
            config: Provider configuration
            
        Returns:
            True if healthy, False otherwise
        """
        try:
            # In real implementation:
            # - Make lightweight API call (e.g., ping endpoint)
            # - Check response time
            # - Verify authentication
            # - Check rate limit status
            
            # Simulated health check
            await asyncio.sleep(0.1)
            return True
        except Exception:
            return False
    
    def _calculate_health_status(
        self,
        config: ProviderConfig,
        metrics: ProviderHealthMetrics
    ) -> ProviderHealthStatus:
        """
        Calculate health status from metrics.
        
        Args:
            config: Provider configuration
            metrics: Health metrics
            
        Returns:
            ProviderHealthStatus
        """
        # Check consecutive failures
        if metrics.consecutive_failures >= config.max_consecutive_failures:
            return ProviderHealthStatus.UNHEALTHY
        
        # Check error rate
        if metrics.error_rate > config.error_rate_threshold:
            return ProviderHealthStatus.UNHEALTHY
        
        # Check latency
        if metrics.avg_latency > config.latency_threshold:
            return ProviderHealthStatus.DEGRADED
        
        # Check success rate
        if metrics.success_rate < 0.9:
            return ProviderHealthStatus.DEGRADED
        
        return ProviderHealthStatus.HEALTHY
    
    def record_request_result(
        self,
        provider_id: str,
        success: bool,
        latency: float
    ):
        """
        Record request result for health tracking.
        
        Args:
            provider_id: Provider identifier
            success: Whether request succeeded
            latency: Request latency in seconds
        """
        if provider_id not in self.health_metrics:
            return
        
        metrics = self.health_metrics[provider_id]
        metrics.total_requests += 1
        
        if not success:
            metrics.total_errors += 1
            metrics.consecutive_failures += 1
        else:
            metrics.consecutive_failures = 0
        
        # Update average latency
        history = self.request_history[provider_id]
        history.append(latency)
        if len(history) > 0:
            metrics.avg_latency = sum(history) / len(history)
        
        # Update success rate
        metrics.success_rate = 1.0 - (metrics.total_errors / metrics.total_requests)
        metrics.error_rate = metrics.total_errors / metrics.total_requests
        
        # Recalculate health status
        if provider_id in self.providers:
            config = self.providers[provider_id]
            self.health_status[provider_id] = self._calculate_health_status(
                config, metrics
            )
    
    def get_health_status(
        self,
        provider_id: str
    ) -> ProviderHealthStatus:
        """
        Get current health status.
        
        Args:
            provider_id: Provider identifier
            
        Returns:
            ProviderHealthStatus
        """
        return self.health_status.get(
            provider_id,
            ProviderHealthStatus.UNHEALTHY
        )
    
    def get_healthy_providers(
        self
    ) -> List[str]:
        """
        Get list of healthy providers.
        
        Returns:
            List of healthy provider IDs
        """
        return [
            pid for pid, status in self.health_status.items()
            if status == ProviderHealthStatus.HEALTHY
        ]


# ============================================================================
# Multi-Provider Router
# ============================================================================

class LoadBalancingStrategy(Enum):
    """
    Load balancing strategies.
    
    This demonstrates routing patterns:
    - Round-robin: Even distribution
    - Weighted: Based on capacity/cost
    - Least connections: Fewest active
    - Health-based: Only healthy providers
    """
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    HEALTH_BASED = "health_based"


@dataclass
class ProviderRequest:
    """
    Provider request result.
    
    This demonstrates request tracking:
    - Provider used
    - Success status
    - Response data
    - Latency
    - Cost
    """
    provider_id: str
    success: bool
    response: Optional[Any] = None
    error: Optional[Exception] = None
    latency: float = 0.0
    cost: float = 0.0


class MultiProviderRouter:
    """
    Router for multi-provider failover.
    
    This demonstrates failover patterns:
    - Provider selection
    - Automatic failover
    - Load balancing
    - Cost tracking
    """
    
    def __init__(
        self,
        providers: List[ProviderConfig],
        health_monitor: ProviderHealthMonitor,
        load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.HEALTH_BASED
    ):
        """
        Initialize router.
        
        Args:
            providers: List of provider configurations
            health_monitor: Health monitor instance
            load_balancing: Load balancing strategy
        """
        self.providers = sorted(providers, key=lambda p: p.priority)
        self.health_monitor = health_monitor
        self.load_balancing = load_balancing
        self.active_connections: Dict[str, int] = {
            p.provider_id: 0 for p in providers
        }
        self.round_robin_index: Dict[str, int] = {
            p.provider_id: 0 for p in providers
        }
        self.cost_tracking: Dict[str, float] = {
            p.provider_id: 0.0 for p in providers
        }
    
    async def route_request(
        self,
        request_data: Dict[str, Any],
        max_retries: int = 3
    ) -> ProviderRequest:
        """
        Route request with failover.
        
        Args:
            request_data: Request data
            max_retries: Maximum retry attempts
            
        Returns:
            ProviderRequest result
        """
        # Select initial provider
        provider = self._select_provider()
        
        if not provider:
            return ProviderRequest(
                provider_id="",
                success=False,
                error=Exception("No healthy providers available")
            )
        
        # Try providers in priority order
        for attempt in range(max_retries):
            if attempt > 0:
                # Select next provider in failover chain
                provider = self._select_next_provider(provider.provider_id)
                if not provider:
                    break
            
            # Execute request
            result = await self._execute_request(provider, request_data)
            
            # Record result for health monitoring
            self.health_monitor.record_request_result(
                provider.provider_id,
                result.success,
                result.latency
            )
            
            # Track cost
            if result.success:
                self.cost_tracking[provider.provider_id] += result.cost
            
            # If successful, return result
            if result.success:
                return result
            
            # If transient error, retry with same provider
            if self._is_transient_error(result.error):
                continue
            
            # If permanent error, failover to next provider
            break
        
        # All providers failed
        return ProviderRequest(
            provider_id=provider.provider_id if provider else "",
            success=False,
            error=Exception("All providers failed")
        )
    
    def _select_provider(
        self
    ) -> Optional[ProviderConfig]:
        """
        Select provider based on load balancing strategy.
        
        Returns:
            Selected provider configuration
        """
        healthy_providers = [
            p for p in self.providers
            if self.health_monitor.get_health_status(p.provider_id) == ProviderHealthStatus.HEALTHY
        ]
        
        if not healthy_providers:
            return None
        
        if self.load_balancing == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin_select(healthy_providers)
        elif self.load_balancing == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections_select(healthy_providers)
        elif self.load_balancing == LoadBalancingStrategy.HEALTH_BASED:
            return healthy_providers[0]  # Highest priority healthy provider
        else:
            return healthy_providers[0]
    
    def _round_robin_select(
        self,
        providers: List[ProviderConfig]
    ) -> ProviderConfig:
        """
        Select provider using round-robin.
        
        Args:
            providers: List of available providers
            
        Returns:
            Selected provider
        """
        if not providers:
            return None
        
        # Use first provider's index for simplicity
        index = self.round_robin_index.get(providers[0].provider_id, 0)
        selected = providers[index % len(providers)]
        self.round_robin_index[providers[0].provider_id] = (index + 1) % len(providers)
        return selected
    
    def _least_connections_select(
        self,
        providers: List[ProviderConfig]
    ) -> ProviderConfig:
        """
        Select provider with least connections.
        
        Args:
            providers: List of available providers
            
        Returns:
            Selected provider
        """
        if not providers:
            return None
        
        return min(
            providers,
            key=lambda p: self.active_connections.get(p.provider_id, 0)
        )
    
    def _select_next_provider(
        self,
        current_provider_id: str
    ) -> Optional[ProviderConfig]:
        """
        Select next provider in failover chain.
        
        Args:
            current_provider_id: Current provider ID
            
        Returns:
            Next provider in chain
        """
        current_index = next(
            (i for i, p in enumerate(self.providers) if p.provider_id == current_provider_id),
            -1
        )
        
        if current_index == -1:
            return None
        
        # Try next providers in priority order
        for i in range(current_index + 1, len(self.providers)):
            provider = self.providers[i]
            status = self.health_monitor.get_health_status(provider.provider_id)
            if status != ProviderHealthStatus.UNHEALTHY:
                return provider
        
        return None
    
    async def _execute_request(
        self,
        provider: ProviderConfig,
        request_data: Dict[str, Any]
    ) -> ProviderRequest:
        """
        Execute request with provider.
        
        Args:
            provider: Provider configuration
            request_data: Request data
            
        Returns:
            ProviderRequest result
        """
        start_time = datetime.now()
        self.active_connections[provider.provider_id] += 1
        
        try:
            # In real implementation:
            # - Make API call to provider
            # - Handle authentication
            # - Parse response
            # - Calculate cost
            
            # Simulated request
            await asyncio.sleep(0.1)
            
            latency = (datetime.now() - start_time).total_seconds()
            
            return ProviderRequest(
                provider_id=provider.provider_id,
                success=True,
                response={"result": "success"},
                latency=latency,
                cost=0.001  # Example cost
            )
        except Exception as e:
            latency = (datetime.now() - start_time).total_seconds()
            return ProviderRequest(
                provider_id=provider.provider_id,
                success=False,
                error=e,
                latency=latency
            )
        finally:
            self.active_connections[provider.provider_id] = max(
                0,
                self.active_connections[provider.provider_id] - 1
            )
    
    def _is_transient_error(
        self,
        error: Optional[Exception]
    ) -> bool:
        """
        Check if error is transient.
        
        Args:
            error: Exception to check
            
        Returns:
            True if transient, False if permanent
        """
        if not error:
            return False
        
        # In real implementation:
        # - Check HTTP status codes (429, 503, 502 = transient)
        # - Check error types (timeout = transient)
        # - Check error messages
        
        return True  # Simplified
    
    def get_cost_summary(
        self
    ) -> Dict[str, float]:
        """
        Get cost summary per provider.
        
        Returns:
            Dictionary of provider_id -> total cost
        """
        return self.cost_tracking.copy()
