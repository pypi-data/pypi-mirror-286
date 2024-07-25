"""Utility functions for micpy."""

import sys
import time


def convert_si(value, unit_in, unit_out):
    """Convert value from one SI unit to another SI unit."""
    SI = {"μm": 0.000001, "mm": 0.001, "cm": 0.01, "m": 1.0}

    if isinstance(value, (float, int)):
        return value * SI[unit_in] / SI[unit_out]
    elif isinstance(value, (tuple, list)):
        return [v * SI[unit_in] / SI[unit_out] for v in value]
    raise ValueError("Unsupported value type.")


def progress_indicator(iterable, description="Progress", unit="Iteration", start=1):
    """Progress indicator for iterable."""

    start_time = time.time()

    for i, item in enumerate(iterable, start=start):
        yield item

        elapsed_time = time.time() - start_time
        average_time = elapsed_time / i

        message = f"\r{description}: {unit} {i}. Elapsed Time: {elapsed_time:.2f}s. Average Time/{unit}: {average_time:.2f}s"

        sys.stdout.write("\r\x1b[0K")  # Clear line
        print(message, end="")
        sys.stdout.flush()

    print("")
    sys.stdout.flush()


def is_compressed(filename):
    """Check if a file is compressed."""

    with open(filename, "rb") as f:
        return f.read(2) == b"\x1f\x8b"  # gzip magic number
