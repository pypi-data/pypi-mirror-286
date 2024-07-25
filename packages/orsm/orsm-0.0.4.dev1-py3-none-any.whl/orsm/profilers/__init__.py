"""
Profiling decorators.
"""
from orsm.profilers.memory.memory_profilers import profile_memory
from orsm.profilers.time.time_profilers import profile_time
from orsm.decorators.disabling import disable_decorator
from orsm.cli import cli
from orsm.profilers.memory.memory_profilers import memory_profiler
from orsm.profilers.time.time_profilers import time_profiler
import atexit

profile_memory, profile_time = [disable_decorator(cli.profiling_disabled, reason="Profiling has not been enabled from the command line.")(f) for f in [profile_memory, profile_time]]

@atexit.register
def print_profilers():
    if not cli.profiling_disabled():
        time_profiler.print_stats(output_unit=1e-3)
        memory_profiler.print_stats()