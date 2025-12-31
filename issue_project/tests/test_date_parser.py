"""
Tests for DateParser module

These tests demonstrate the browser compatibility issue:
- Chrome/Edge format (ISO 8601) works correctly
- Safari/Firefox alternative formats fail
"""

import pytest
from datetime import datetime
from src.date_parser import DateParser, DateParseError


class TestDateParserChromeEdge:
    """Tests for Chrome/Edge datetime-local format (ISO 8601) - SHOULD PASS"""
    
    def test_parse_chrome_edge_format(self):
        """Test that Chrome/Edge ISO 8601 format works correctly"""
        parser = DateParser()
        
        # Chrome/Edge datetime-local produces ISO 8601 format
        date_string = "2024-06-15T14:30"
        result = parser.parse_event_datetime(date_string)
        
        assert result.year == 2024
        assert result.month == 6
        assert result.day == 15
        assert result.hour == 14
        assert result.minute == 30
    
    def test_parse_chrome_edge_with_seconds(self):
        """Test ISO format with seconds"""
        parser = DateParser()
        
        date_string = "2024-12-25T09:00:00"
        result = parser.parse_event_datetime(date_string)
        
        assert result.year == 2024
        assert result.month == 12
        assert result.day == 25
        assert result.hour == 9
        assert result.minute == 0


class TestDateParserSafariBrowserIssues:
    """
    Tests for Safari browser compatibility issues - CURRENTLY FAILING
    
    These tests demonstrate the bug: Safari users who manually enter dates
    in common formats will fail because the parser only accepts ISO 8601.
    
    These tests will FAIL until the bug is fixed!
    """
    
    @pytest.mark.xfail(reason="BUG: Parser only accepts ISO format, rejects Safari slash format", strict=True)
    def test_parse_safari_slash_format(self):
        """
        CURRENTLY FAILS: Safari users often enter dates with slashes
        
        BUG LOCATION: src/date_parser.py, line 47-54 (parse_event_datetime method)
        TRIGGER: When Safari user manually types date as "2024/01/15 14:30"
        EXPECTED: Should parse successfully and return datetime(2024, 1, 15, 14, 30)
        ACTUAL: Raises DateParseError because only ISO format is supported
        """
        parser = DateParser()
        
        # Safari user manually enters date with slashes
        date_string = "2024/01/15 14:30"
        
        # This SHOULD work - test expects success
        result = parser.parse_event_datetime(date_string)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 14
        assert result.minute == 30
    
    @pytest.mark.xfail(reason="BUG: Parser rejects US format with AM/PM", strict=True)
    def test_parse_safari_us_format_with_am_pm(self):
        """
        CURRENTLY FAILS: Safari users in US locale might use MM/DD/YYYY with AM/PM
        
        BUG LOCATION: src/date_parser.py, line 47-54 (parse_event_datetime method)
        TRIGGER: When user types "01/15/2024 02:30 PM"
        EXPECTED: Should parse to datetime(2024, 1, 15, 14, 30)
        ACTUAL: Raises DateParseError
        """
        parser = DateParser()
        
        # Common US date format with AM/PM
        date_string = "01/15/2024 02:30 PM"
        
        # This SHOULD work - expecting 2:30 PM = 14:30 in 24-hour format
        result = parser.parse_event_datetime(date_string)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 14  # 2:30 PM = 14:30
        assert result.minute == 30


class TestDateParserFirefoxBrowserIssues:
    """
    Tests for Firefox browser compatibility issues - CURRENTLY FAILING
    
    Firefox (especially older versions) doesn't support datetime-local,
    forcing users to manually enter dates.
    
    These tests will FAIL until the bug is fixed!
    """
    
    @pytest.mark.xfail(reason="BUG: Parser rejects text month format", strict=True)
    def test_parse_firefox_text_month_format(self):
        """
        CURRENTLY FAILS: Firefox users might enter dates with text month names
        
        BUG LOCATION: src/date_parser.py, line 47-54 (parse_event_datetime method)
        TRIGGER: When user types "Jan 15, 2024 14:30"
        EXPECTED: Should parse successfully
        ACTUAL: Raises DateParseError
        """
        parser = DateParser()
        
        # Firefox user enters date with text month
        date_string = "Jan 15, 2024 14:30"
        
        # This SHOULD work - test expects success
        result = parser.parse_event_datetime(date_string)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 14
        assert result.minute == 30
    
    @pytest.mark.xfail(reason="BUG: Parser rejects European DD-MM-YYYY format", strict=True)
    def test_parse_firefox_european_format(self):
        """
        CURRENTLY FAILS: European Firefox users use DD-MM-YYYY format
        
        BUG LOCATION: src/date_parser.py, line 47-54 (parse_event_datetime method)
        TRIGGER: When user types "15-01-2024 14:30"
        EXPECTED: Should parse to datetime(2024, 1, 15, 14, 30)
        ACTUAL: Raises DateParseError
        """
        parser = DateParser()
        
        # European date format (day-month-year)
        date_string = "15-01-2024 14:30"
        
        # This SHOULD work - test expects success
        result = parser.parse_event_datetime(date_string)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 14
        assert result.minute == 30


class TestDateParserEdgeCases:
    """Test edge cases and validation"""
    
    def test_empty_string_raises_error(self):
        """Test that empty string raises appropriate error"""
        parser = DateParser()
        
        with pytest.raises(DateParseError) as exc_info:
            parser.parse_event_datetime("")
        
        assert "cannot be empty" in str(exc_info.value)
    
    def test_none_value_raises_error(self):
        """Test that None value raises appropriate error"""
        parser = DateParser()
        
        with pytest.raises(DateParseError):
            parser.parse_event_datetime(None)
    
    def test_format_for_display(self):
        """Test datetime display formatting"""
        parser = DateParser()
        
        dt = datetime(2024, 6, 15, 14, 30)
        result = parser.format_for_display(dt)
        
        assert "June 15, 2024" in result
        assert "02:30 PM" in result
