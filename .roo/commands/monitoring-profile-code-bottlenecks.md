---
description: "Run a **Python profiler** (e.g. `cProfile`, `pyinstrument`) on a representative workload. Measure before optimizing: find 1\u20132 hot functions, assess complexity, refactor, re-measure."
---

# Profile Code Bottlenecks

## Overview

Run a **Python profiler** (e.g. `cProfile`, `pyinstrument`) on a representative workload. Measure before optimizing: find 1–2 hot functions, assess complexity, refactor, re-measure.

## Scope and boundaries

- **In scope:** CPU/time profiling of Python code paths.
- **Out of scope — use instead:** Distributed trace analytics → `/monitoring-analyze-langsmith-traces`. Infra/service metrics → `/monitoring-performance-analysis`.

## Rules Applied

- `core-python-standards`
- `monitoring-and-observability`

## Steps

1. **Identify Target Code**
   - Determine the module, script, or entry point to profile
   - Identify the workload or scenario to run (e.g., typical request, batch job)
   - Ensure the target code path is representative of production load

2. **Run Profiler**
   - Execute `cProfile` (or `pyinstrument`, `yappi` on Python code) on the target
   - Use appropriate invocation: `python -m cProfile -o profile_output.stats script.py` or `cProfile.run()` in code
   - Run with representative input data or workload

3. **Analyze Profiler Output**
   - **totTime (total time)**: Identify functions consuming the most runtime per call
   - **nCalls**: Count how often each function is invoked—high frequency may indicate algorithmic inefficiency
   - **cumTime (cumulative time)**: Identify functions with the highest total time including callees
   - Sort by `totTime` or `cumTime` to find the top 1–2 bottleneck functions

4. **Assess Algorithmic Complexity**
   - For each bottleneck function, analyze its Big-O complexity
   - Identify nested loops (e.g., loop inside loop → O(n²) or worse)
   - Check for redundant work, repeated calls, or unnecessary data structures
   - Consider data size impact: code that works on small data often fails at scale due to wrong algorithmic complexity, not infrastructure or database

5. **Prioritize and Refactor**
   - Focus on the 1–2 functions with highest impact
   - Propose targeted refactor (e.g., reduce complexity, add caching, optimize loops)
   - Avoid premature optimization of non-bottleneck code

6. **Validate Improvement**
   - Re-run profiler after refactor
   - Compare before/after metrics (totTime, cumTime, nCalls)
   - Report measurable improvement

## Data Sources
- Target Python source files (modules, scripts, entry points)
- Profiler output (e.g., `cProfile` `.stats` files, `pstats` output)
- Representative workload or test data used during profiling

## Output
A profiling report including:
- **Bottleneck Summary**: Top 1–2 functions by totTime or cumTime with nCalls
- **Complexity Analysis**: Big-O assessment for each bottleneck function
- **Root Cause**: Whether the issue is algorithmic (e.g., O(n²)), infrastructure, or data-related
- **Refactor Recommendations**: Prioritized, targeted optimization steps
- **Before/After Metrics**: If refactor was applied, comparison of profiler metrics
