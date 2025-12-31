"""
Date Parser Module for Event Registration System

This module handles date/time parsing from different browser inputs.

FIXED: Now supports multiple common date formats using dateutil.parser
for better browser compatibility (Chrome/Edge, Safari, Firefox).
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
    
    FIXED: Now uses dateutil.parser to handle multiple common formats:
    - ISO 8601 (Chrome/Edge): "2024-01-15T10:00"
    - Slash format (Safari): "2024/01/15 10:00"
    - US format with AM/PM: "01/15/2024 10:00 AM"
    - Text month (Firefox): "Jan 15, 2024 10:00"
    - European format: "15-01-2024 10:00"
    """
    
    @staticmethod
    def parse_event_datetime(date_string: str) -> datetime:
        """
        Parse event date/time from form submission.
        
        Args:
            date_string: Date time string from browser input
            
        Returns:
            datetime object
            
        Raises:
            DateParseError: If date format is not recognized
            
        Supported formats:
            - Chrome/Edge: "2024-01-15T10:00" (datetime-local ISO format)
            - Safari: "2024/01/15 10:00", "01/15/2024 10:00 AM"
            - Firefox: "Jan 15, 2024 10:00", "15-01-2024 10:00"
        """
        if not date_string or not isinstance(date_string, str):
            raise DateParseError("Date string cannot be empty or non-string")
        
        date_string = date_string.strip()
        
        # FIXED: Use dateutil.parser for robust multi-format parsing
        # This handles ISO 8601, slash formats, AM/PM, text months, etc.
        try:
            parsed_date = dateutil_parser.parse(date_string)
            return parsed_date
        except (ValueError, dateutil_parser.ParserError):
            raise DateParseError(
                f"Could not parse date: '{date_string}'. "
                f"Supported formats include ISO 8601 (2024-01-15T10:00), "
                f"slash format (2024/01/15 10:00), US format (01/15/2024 10:00 AM), "
                f"text month (Jan 15, 2024 10:00), and European format (15-01-2024 10:00)"
            )
    
    @staticmethod
    def format_for_display(dt: datetime) -> str:
        """Format datetime for display to user"""
        return dt.strftime("%B %d, %Y at %I:%M %p")
