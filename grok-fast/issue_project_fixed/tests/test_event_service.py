"""
Tests for EventService module

These tests demonstrate how browser compatibility issues affect
the entire registration flow.
"""

import pytest
from datetime import datetime, timedelta
from src.event_service import EventService, RegistrationError


class TestEventServiceWithChromeEdge:
    """Tests with Chrome/Edge compatible date formats - SHOULD PASS"""
    
    def test_successful_registration_chrome_format(self):
        """Test successful registration with Chrome/Edge ISO format"""
        service = EventService()
        
        # Future date in ISO format (Chrome/Edge datetime-local output)
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")
        
        result = service.register_participant(
            name="John Doe",
            email="john@example.com",
            event_datetime=future_date
        )
        
        assert result["success"] is True
        assert "John Doe" in result["message"]
        assert service.get_registration_count() == 1
    
    def test_multiple_registrations_chrome_format(self):
        """Test multiple registrations with valid ISO format"""
        service = EventService()
        
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")
        
        service.register_participant(
            name="Alice",
            email="alice@example.com",
            event_datetime=future_date
        )
        
        service.register_participant(
            name="Bob",
            email="bob@example.com",
            event_datetime=future_date
        )
        
        assert service.get_registration_count() == 2
        registrations = service.get_registrations()
        assert len(registrations) == 2
        assert registrations[0]["name"] == "Alice"
        assert registrations[1]["name"] == "Bob"


class TestEventServiceSafariBrowserIssues:
    """
    Tests demonstrating Safari browser compatibility issues - NOW FIXED
    
    Safari users can now manually enter dates in various formats
    and registration will succeed.
    
    All tests should now PASS!
    """
    
    def test_registration_fails_with_safari_slash_format(self):
        """
        FIXED: Safari user with slash-formatted date can now register successfully
        
        FLOW:
        1. Safari user manually enters: "2024/06/15 14:30"
        2. EventService calls DateParser.parse_event_datetime()
        3. DateParser now uses dateutil.parser, accepts the format
        4. Registration succeeds
        
        TRIGGER: Safari user submits form with manual date entry
        EXPECTED: Registration should succeed
        ACTUAL: Registration now succeeds
        """
        service = EventService()
        
        # Safari user manually enters date with slashes (30 days in future)
        future_date = (datetime.now() + timedelta(days=30))
        safari_date = future_date.strftime("%Y/%m/%d %H:%M")
        
        # This SHOULD work - registration should succeed
        result = service.register_participant(
            name="Safari User",
            email="safari@example.com",
            event_datetime=safari_date
        )
        
        assert result["success"] is True
        assert "Safari User" in result["message"]
        assert service.get_registration_count() == 1
    
    def test_registration_fails_with_us_date_format(self):
        """
        FIXED: US-locale Safari user with MM/DD/YYYY format can now register
        
        TRIGGER: User submits "06/15/2025 02:30 PM"
        EXPECTED: Successful registration
        ACTUAL: Registration now succeeds
        """
        service = EventService()
        
        # US format with AM/PM (common Safari manual entry)
        us_date = "06/15/2026 02:30 PM"
        
        # This SHOULD work - registration should succeed
        result = service.register_participant(
            name="US User",
            email="us@example.com",
            event_datetime=us_date
        )
        
        assert result["success"] is True
        assert service.get_registration_count() == 1


class TestEventServiceFirefoxBrowserIssues:
    """
    Tests demonstrating Firefox browser compatibility issues - NOW FIXED
    """
    
    def test_registration_fails_with_firefox_text_month(self):
        """
        FAILING TEST: Firefox user with text month format rejected
        
        BUG LOCATION: src/date_parser.py, line 47-54
        TRIGGER: User submits "Jun 15, 2025 14:30"
        EXPECTED: Successful registration
        ACTUAL: RegistrationError raisedCURRENTLY FAILING
    
    These tests will FAIL until the bug is fixed!
    """
    
    def test_registration_fails_with_firefox_text_month(self):
        """
        FIXED: Firefox user with text month format can now register
        
        TRIGGER: User submits "Jun 15, 2025 14:30"
        EXPECTED: Successful registration
        ACTUAL: Registration now succeeds
        """
        service = EventService()
        
        # Text month format (common Firefox manual entry)
        firefox_date = "Jun 15, 2026 14:30"
        
        # This SHOULD work - registration should succeed
        result = service.register_participant(
            name="Firefox User",
            email="firefox@example.com",
            event_datetime=firefox_date
        )
        
        assert result["success"] is True
        assert service.get_registration_count() == 1
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
        
        with pytest.raises(RegistrationError) as exc_info:
            service.register_participant(
                name="Time Traveler",
                email="past@example.com",
                event_datetime=past_date
            )
        
        assert "past events" in str(exc_info.value).lower()
    
    def test_registration_fails_without_name(self):
        """Test that name is required"""
        service = EventService()
        
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")
        
        with pytest.raises(RegistrationError) as exc_info:
            service.register_participant(
                name="",
                email="test@example.com",
                event_datetime=future_date
            )
        
        assert "required" in str(exc_info.value).lower()
    
    def test_registration_fails_without_email(self):
        """Test that email is required"""
        service = EventService()
        
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")
        
        with pytest.raises(RegistrationError) as exc_info:
            service.register_participant(
                name="Test User",
                email="",
                event_datetime=future_date
            )
        
        assert "required" in str(exc_info.value).lower()
