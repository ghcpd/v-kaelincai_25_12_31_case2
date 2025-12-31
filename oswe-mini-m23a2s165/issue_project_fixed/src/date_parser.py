"""
Date Parser Module for Event Registration System (fixed)

This version accepts multiple common date/time formats so Safari/Firefox
manual entries are handled correctly while remaining backward-compatible
with ISO 8601 produced by Chrome/Edge `datetime-local`.
"""

from datetime import datetime
from typing import Optional

from dateutil import parser as _du_parser


class DateParseError(Exception):
    """Raised when date parsing fails"""
    pass


class DateParser:
    """
    Parses date strings from browser form submissions.

    The fixed parser keeps the original ISO handling but adds robust
    fallback parsing using python-dateutil to accept a variety of
    commonly-entered formats (slash format, AM/PM, text-months, European).
    """

    @staticmethod
    def parse_event_datetime(date_string: str) -> datetime:
        """
        Parse event date/time from form submission.

        Supports (non-exhaustive):
          - ISO 8601: "2024-01-15T10:00" or with seconds
          - Slash formats: "2024/06/15 14:30"
          - US with AM/PM: "06/15/2024 02:30 PM"
          - Text month: "Jun 15, 2024 14:30"
          - European (DD-MM-YYYY): "15-06-2024 14:30"

        Keeps the same function signature and raises DateParseError on failure.
        """
        if not date_string or not isinstance(date_string, str):
            raise DateParseError("Date string cannot be empty or non-string")

        s = date_string.strip()

        # Fast path: preserve original ISO 8601 behaviour (keeps backward compat)
        try:
            return datetime.fromisoformat(s)
        except Exception:
            pass

        # Fallbacks: use python-dateutil which handles a wide range of formats.
        # Try default (month-first) then day-first for European-style inputs.
        parse_attempts = [dict(dayfirst=False), dict(dayfirst=True)]
        for opts in parse_attempts:
            try:
                dt = _du_parser.parse(s, **opts)
                return dt
            except (ValueError, OverflowError):
                continue

        # If we reach here, parsing failed for all supported formats
        raise DateParseError(
            f"Invalid date format: '{date_string}'. Supported formats include ISO (YYYY-MM-DDTHH:MM), "
            f"'YYYY/MM/DD HH:MM', 'MM/DD/YYYY HH:MM AM/PM', 'DD-MM-YYYY HH:MM', or textual months like 'Jun 15, 2024 14:30'."
        )

    @staticmethod
    def format_for_display(dt: datetime) -> str:
        """Format datetime for display to user"""
        return dt.strftime("%B %d, %Y at %I:%M %p")
