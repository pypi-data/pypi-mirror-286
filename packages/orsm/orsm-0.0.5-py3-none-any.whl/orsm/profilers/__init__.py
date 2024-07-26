"""
Profiling decorators.
"""
from orsm.profilers.memory.memory_profilers import profile_memory, memory_profiler
from orsm.profilers.time.time_profilers import profile_time, time_profiler

_profilers = [memory_profiler, time_profiler]
