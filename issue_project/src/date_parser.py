"""
Date Parser Module for Event Registration System

This module handles date/time parsing from different browser inputs.

KNOWN ISSUE: Currently only supports ISO 8601 format (datetime-local from Chrome/Edge).
Safari and Firefox users may submit different formats that cause parsing failures.
"""

from datetime import datetime
from typing import Optional


class DateParseError(Exception):
    """Raised when date parsing fails"""
    pass


class DateParser:
    """
    Parses date strings from browser form submissions.
    
    BUG: Only supports ISO 8601 format (YYYY-MM-DDTHH:MM).
    Does not handle alternative formats from Safari/Firefox users who
    manually enter dates in different formats.
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
            
        Expected formats:
            - Chrome/Edge: "2024-01-15T10:00" (datetime-local ISO format)
            
        Problematic formats (currently NOT supported):
            - Safari manual entry: "2024/01/15 10:00", "01/15/2024 10:00 AM"
            - Firefox manual entry: "Jan 15, 2024 10:00", "15-Jan-2024 10:00"
        """
        if not date_string or not isinstance(date_string, str):
            raise DateParseError("Date string cannot be empty or non-string")
        
        date_string = date_string.strip()
        
        # BUG: Only tries ISO 8601 format (datetime-local standard)
        # This works for Chrome/Edge with native datetime-local picker
        # But fails for Safari/Firefox where users manually type dates
        try:
            # Try ISO 8601 format: "2024-01-15T10:00"
            parsed_date = datetime.fromisoformat(date_string)
            return parsed_date
        except ValueError:
            # BUG: No fallback parsing for other common formats
            raise DateParseError(
                f"Invalid date format: '{date_string}'. "
                f"Expected ISO 8601 format (YYYY-MM-DDTHH:MM), "
                f"e.g., '2024-01-15T10:00'"
            )
    
    @staticmethod
    def format_for_display(dt: datetime) -> str:
        """Format datetime for display to user"""
        return dt.strftime("%B %d, %Y at %I:%M %p")
