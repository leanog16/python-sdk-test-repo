"""
report.py

Build per-account usage summaries from the call log

@copyright Bandwidth INC
"""
from typing import Dict, List

from .call_log import CallLog
from .formatting import format_number


def summarize_accounts(log: CallLog, account_ids: List[str],
                       country_code: str = "+1") -> Dict[str, Dict]:
    """Summarize call usage for several accounts

    Args:
        log (CallLog): The call log to read from
        account_ids (list[str]): The accounts to summarize
        country_code (str, optional): Prefix used when formatting numbers. Defaults to "+1".

    Returns:
        dict: Maps each account id to {"calls", "total_seconds", "numbers"}
    """
    summary = {}
    for account_id in account_ids:
        calls = log.find_by_account(account_id)
        summary[account_id] = {
            "calls": len(calls),
            "total_seconds": sum(call["duration"] for call in calls),
            "numbers": sorted({format_number(call["to_number"], country_code=country_code)
                               for call in calls}),
        }
    return summary
