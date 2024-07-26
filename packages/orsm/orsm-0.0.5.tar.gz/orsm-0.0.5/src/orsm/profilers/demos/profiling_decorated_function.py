from orsm.cli import cli
from orsm.profilers.time.time_profilers import profile_time
from orsm.profilers.memory.memory_profilers import profile_memory

if __name__ == "__main__":
    parser = cli.setup_standard_parser()
    parser.parse_args(["--profiling"])

    @profile_memory
    @profile_time
    def some_example():
        import time
        for i in range(5):
            time.sleep(0.1)

    some_example()