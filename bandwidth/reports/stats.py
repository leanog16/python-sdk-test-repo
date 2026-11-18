"""
stats.py

Concurrent processing of call records

@copyright Bandwidth INC
"""
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List


processed_count = 0


def _minutes(call: Dict) -> int:
    """Round a call's duration up to whole billable minutes
    """
    global processed_count
    processed_count += 1
    return (call["duration"] + 59) // 60


def process_batch(calls: List[Dict], workers: int = 4) -> List[int]:
    """Compute billable minutes for each call using a thread pool

    Args:
        calls (list[dict]): Call records with a "duration" in seconds
        workers (int, optional): Number of worker threads. Defaults to 4.

    Returns:
        list[int]: Billable minutes, in the same order as calls
    """
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_minutes, calls))
