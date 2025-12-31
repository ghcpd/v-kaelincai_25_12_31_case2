"""
Date Parser Module for Event Registration System (fixed)

This module now accepts multiple common date/time formats submitted by
different browsers (Chrome/Edge, Safari, Firefox) while maintaining
backwards compatibility with ISO 8601 produced by `datetime-local`.
"""
from datetime import datetime
from typing import Optional

from dateutil import parser as dateutil_parser


class DateParseError(Exception):
    """Raised when date parsing fails"""


class DateParser:
    """
    Robust date/time parser for event submissions.

    Accepts multiple common formats (keeps ISO support):
      - ISO 8601: "2024-06-15T14:30" (with or without seconds)
      - Slash format: "2024/06/15 14:30"
      - US format w/ AM/PM: "06/15/2024 02:30 PM"
      - Text month: "Jun 15, 2024 14:30"
      - European: "15-06-2024 14:30"

    Implementation notes:
    - Fast-path with datetime.fromisoformat for exact ISO inputs
    - Fallback to dateutil.parser.parse with sensible options
    - Second fallback tries day-first parsing for ambiguous/European
    - Returns naive datetime (tests and app expect naive datetimes)
    - Raises DateParseError on invalid input
    """

    @staticmethod
    def parse_event_datetime(date_string: str) -> datetime:
        """
        Parse event date/time from form submission.

        Args:
            date_string: Date time string from browser input

        Returns:
            datetime object (naive)

        Raises:
            DateParseError: If date format is not recognized or input invalid
        """
        if not date_string or not isinstance(date_string, str):
            raise DateParseError("Date string cannot be empty or non-string")

        date_string = date_string.strip()

        # 1) Fast-path: exact ISO formats (keeps original behavior & perf)
        try:
            parsed_date = datetime.fromisoformat(date_string)
            return parsed_date
        except Exception:
            # continue to flexible parsing
            pass

        # 2) Flexible parsing using python-dateutil
        # Try without dayfirst (common US/ISO/text-month interpretations)
        parse_attempts = []
        try:
            parsed = dateutil_parser.parse(date_string, fuzzy=False)
            # convert aware -> naive by dropping tzinfo (app uses naive)
            if parsed.tzinfo is not None:
                parsed = parsed.replace(tzinfo=None)
            return parsed
        except Exception as e:
            parse_attempts.append(str(e))

        # 3) Try day-first parsing for European-style dates (e.g., 15-06-2024)
        try:
            parsed = dateutil_parser.parse(date_string, dayfirst=True, fuzzy=False)
            if parsed.tzinfo is not None:
                parsed = parsed.replace(tzinfo=None)
            return parsed
        except Exception as e:
            parse_attempts.append(str(e))

        # If we reach here, all parsing attempts failed
        raise DateParseError(
            f"Invalid date format: '{date_string}'. Supported examples: "
            f"'2024-06-15T14:30', '2024/06/15 14:30', '06/15/2024 02:30 PM', "
            f"'Jun 15, 2024 14:30', '15-06-2024 14:30'"
        )

    @staticmethod
    def format_for_display(dt: datetime) -> str:
        """Format datetime for display to user"""
        return dt.strftime("%B %d, %Y at %I:%M %p")
