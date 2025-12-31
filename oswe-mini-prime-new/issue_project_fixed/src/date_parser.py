"""
Date Parser Module for Event Registration System (Fixed)

This module handles date/time parsing from different browser inputs.

Fix: Accepts multiple common date formats in addition to ISO 8601.
"""

from datetime import datetime
from typing import Optional

from dateutil import parser as dateutil_parser


class DateParseError(Exception):
    """Raised when date parsing fails"""
    pass


class DateParser:
    """
    Parses date strings from browser form submissions.
    
    This improved parser attempts multiple strategies to accept common
    date/time formats typed by users in Safari and Firefox while keeping
    backwards compatibility with Chrome/Edge ISO 8601 output.
    """
    
    @staticmethod
    def parse_event_datetime(date_string: str) -> datetime:
        """
        Parse event date/time from form submission.
        
        Tries the following strategies in order:
        1. datetime.fromisoformat for strict ISO inputs (fast path)
        2. dateutil.parser.parse without dayfirst (handles slashes, text months, AM/PM)
        3. dateutil.parser.parse with dayfirst=True (handles DD-MM-YYYY European style)
        
        Raises DateParseError if none succeed.
        """
        if not date_string or not isinstance(date_string, str):
            raise DateParseError("Date string cannot be empty or non-string")

        date_string = date_string.strip()

        # Fast path: strict ISO 8601 using fromisoformat
        try:
            parsed_date = datetime.fromisoformat(date_string)
            return parsed_date
        except Exception:
            # Continue to more flexible parsing
            pass

        # Flexible parsing using python-dateutil
        parse_attempts = []
        try:
            # First, try default parsing (works for slashes, text months, AM/PM)
            parsed = dateutil_parser.parse(date_string, fuzzy=False)
            return parsed
        except Exception as e:
            parse_attempts.append(str(e))

        try:
            # Try with dayfirst=True to support European formats like 15-06-2024
            parsed = dateutil_parser.parse(date_string, dayfirst=True, fuzzy=False)
            return parsed
        except Exception as e:
            parse_attempts.append(str(e))

        # If we get here, all parsing attempts failed
        raise DateParseError(
            f"Invalid date format: '{date_string}'. Supported examples: "
            f"'2024-06-15T14:30', '2024/06/15 14:30', '06/15/2024 02:30 PM', "
            f"'Jun 15, 2024 14:30', '15-06-2024 14:30'"
        )
    
    @staticmethod
    def format_for_display(dt: datetime) -> str:
        """Format datetime for display to user"""
        return dt.strftime("%B %d, %Y at %I:%M %p")
