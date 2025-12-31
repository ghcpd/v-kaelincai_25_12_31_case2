"""
Date Parser Module for Event Registration System

This module handles date/time parsing from different browser inputs.

FIXED: Now supports multiple date formats from different browsers.
Safari and Firefox users can manually enter dates in common formats.
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
    
    FIXED: Now supports multiple date formats:
    - ISO 8601 format (Chrome/Edge)
    - Slash formats (Safari)
    - US format with AM/PM (Safari US locale)
    - Text month format (Firefox)
    - European format (Firefox EU locale)
    """
    
    # Supported date formats, tried in order
    SUPPORTED_FORMATS = [
        "%Y-%m-%dT%H:%M",           # ISO 8601 without seconds (Chrome/Edge)
        "%Y-%m-%dT%H:%M:%S",        # ISO 8601 with seconds
        "%Y/%m/%d %H:%M",           # Safari slash format
        "%m/%d/%Y %I:%M %p",        # US format with AM/PM
        "%d-%m-%Y %H:%M",           # European format
        "%b %d, %Y %H:%M",          # Text month format
        "%B %d, %Y %H:%M",          # Full text month format
    ]
    
    @staticmethod
    def parse_event_datetime(date_string: str) -> datetime:
        """
        Parse event date/time from form submission.
        
        FIXED: Now supports multiple common date formats from different browsers.
        
        Args:
            date_string: Date time string from browser input
            
        Returns:
            datetime object
            
        Raises:
            DateParseError: If date format is not recognized
            
        Supported formats:
            - Chrome/Edge: "2024-01-15T10:00" (ISO 8601)
            - Safari slash: "2024/01/15 10:00"
            - US format: "01/15/2024 02:30 PM"
            - Firefox text month: "Jan 15, 2024 14:30"
            - European format: "15-01-2024 14:30"
        """
        if not date_string or not isinstance(date_string, str):
            raise DateParseError("Date string cannot be empty or non-string")
        
        date_string = date_string.strip()
        
        # Try specific formats first for predictable parsing
        for fmt in DateParser.SUPPORTED_FORMATS:
            try:
                parsed_date = datetime.strptime(date_string, fmt)
                return parsed_date
            except ValueError:
                continue
        
        # If specific formats fail, try dateutil parser as a fallback
        # This is flexible but less predictable
        try:
            parsed_date = dateutil_parser.parse(date_string)
            return parsed_date
        except (ValueError, dateutil_parser.ParserError):
            raise DateParseError(
                f"Invalid date format: '{date_string}'. "
                f"Supported formats: ISO 8601 (2024-01-15T10:00), "
                f"slash format (2024/01/15 10:00), "
                f"US format (01/15/2024 02:30 PM), "
                f"text month (Jan 15, 2024 14:30), "
                f"or European format (15-01-2024 14:30)"
            )
    
    @staticmethod
    def format_for_display(dt: datetime) -> str:
        """Format datetime for display to user"""
        return dt.strftime("%B %d, %Y at %I:%M %p")
