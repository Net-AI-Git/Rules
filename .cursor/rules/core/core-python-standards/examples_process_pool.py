"""
ProcessPoolExecutor Pattern Example for CPU-Bound Tasks

This file demonstrates the ProcessPoolExecutor pattern for CPU-bound operations
including synthetic data generation and agent parallel initialization.
Reference this example from RULE.mdc using @examples_process_pool.py syntax.
"""

import os
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Any
import random

logger = logging.getLogger(__name__)


# ============================================================================
# Module-Level Functions (Required for ProcessPoolExecutor)
# ============================================================================

def generate_synthetic_data_item(seed: int) -> Dict[str, Any]:
    """
    Generate a single synthetic data item.
    
    This function MUST be at module level (not nested) for ProcessPoolExecutor.
    Each process runs this function independently.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        Generated data item dictionary
    """
    random.seed(seed)
    
    return {
        "id": seed,
        "value": random.randint(1, 1000),
        "category": random.choice(["A", "B", "C"]),
        "score": random.uniform(0.0, 100.0),
    }


def initialize_agent_workload(agent_id: int) -> Dict[str, Any]:
    """
    Initialize a single agent with CPU-bound setup tasks.
    
    This simulates CPU-intensive agent initialization (model loading, 
    embedding generation, data preprocessing).
    
    Args:
        agent_id: Unique agent identifier
        
    Returns:
        Agent initialization result
    """
    # Simulate CPU-bound work (model loading, embedding generation)
    result = sum(i * i for i in range(10000))
    
    return {
        "agent_id": agent_id,
        "status": "initialized",
        "checksum": result % 1000,
    }


# ============================================================================
# Parallel Execution Patterns
# ============================================================================

class ParallelDataGenerator:
    """
    Parallel data generation using ProcessPoolExecutor.
    
    This demonstrates the pattern for generating synthetic data
    in parallel across multiple CPU cores.
    """
    
    def __init__(self, max_workers: int = None):
        """
        Initialize parallel data generator.
        
        Args:
            max_workers: Maximum number of worker processes.
                        Defaults to CPU count for optimal performance.
        """
        self.max_workers = max_workers or os.cpu_count()
        logger.info(f"Initialized ProcessPoolExecutor with {self.max_workers} workers")
    
    def generate_batch(
        self,
        num_items: int
    ) -> List[Dict[str, Any]]:
        """
        Generate synthetic data items in parallel.
        
        This demonstrates the mandatory pattern for CPU-bound batch operations:
        - Uses ProcessPoolExecutor instead of sequential for loops
        - Processes items across multiple CPU cores
        - Handles errors gracefully
        
        Args:
            num_items: Number of items to generate
            
        Returns:
            List of generated data items
        """
        results = []
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            futures = {
                executor.submit(generate_synthetic_data_item, i): i
                for i in range(num_items)
            }
            
            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    item_id = futures[future]
                    logger.error(f"Failed to generate item {item_id}: {e}")
        
        return results
    
    def generate_batch_map(
        self,
        num_items: int
    ) -> List[Dict[str, Any]]:
        """
        Generate synthetic data using map() pattern.
        
        Simpler pattern for when all items use the same function.
        
        Args:
            num_items: Number of items to generate
            
        Returns:
            List of generated data items
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            seeds = list(range(num_items))
            results = list(executor.map(generate_synthetic_data_item, seeds))
        
        return results


class ParallelAgentInitializer:
    """
    Parallel agent initialization using ProcessPoolExecutor.
    
    This demonstrates the pattern for initializing multiple agents
    with CPU-bound setup tasks in production systems.
    """
    
    def __init__(self, max_workers: int = None):
        """
        Initialize parallel agent initializer.
        
        Args:
            max_workers: Maximum number of worker processes
        """
        self.max_workers = max_workers or os.cpu_count()
    
    def initialize_agents(
        self,
        agent_ids: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Initialize multiple agents in parallel.
        
        This demonstrates the mandatory pattern for CPU-bound agent initialization:
        - Uses ProcessPoolExecutor for parallel agent setup
        - Handles initialization failures gracefully
        - Returns results in order of completion
        
        Args:
            agent_ids: List of agent IDs to initialize
            
        Returns:
            List of agent initialization results
        """
        results = []
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all agent initialization tasks
            futures = {
                executor.submit(initialize_agent_workload, agent_id): agent_id
                for agent_id in agent_ids
            }
            
            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Agent {result['agent_id']} initialized successfully")
                except Exception as e:
                    agent_id = futures[future]
                    logger.error(f"Failed to initialize agent {agent_id}: {e}")
                    results.append({
                        "agent_id": agent_id,
                        "status": "failed",
                        "error": str(e),
                    })
        
        return results


# ============================================================================
# Production Usage Example
# ============================================================================

def production_data_generation_example():
    """
    Production example: Generate 10,000 synthetic data items in parallel.
    
    This demonstrates the mandatory pattern for production systems:
    - Uses ProcessPoolExecutor with optimal worker count
    - Handles errors gracefully
    - Logs progress and results
    """
    generator = ParallelDataGenerator(max_workers=os.cpu_count())
    
    logger.info("Starting parallel data generation...")
    results = generator.generate_batch(num_items=10000)
    logger.info(f"Generated {len(results)} items successfully")
    
    return results


def production_agent_initialization_example():
    """
    Production example: Initialize 50 agents in parallel.
    
    This demonstrates the mandatory pattern for production agent systems:
    - Uses ProcessPoolExecutor for CPU-bound agent initialization
    - Handles initialization failures gracefully
    - Returns results for all agents
    """
    initializer = ParallelAgentInitializer(max_workers=os.cpu_count())
    
    agent_ids = list(range(50))
    logger.info(f"Initializing {len(agent_ids)} agents in parallel...")
    
    results = initializer.initialize_agents(agent_ids)
    
    successful = sum(1 for r in results if r.get("status") == "initialized")
    logger.info(f"Successfully initialized {successful}/{len(results)} agents")
    
    return results
