import time


def run_with_time(function_to_run, *values):
    start_time = time.perf_counter()
    result = function_to_run(*values)
    end_time = time.perf_counter()

    return result, round(end_time - start_time, 6)
