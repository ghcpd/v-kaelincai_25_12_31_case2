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
    Tests demonstrating Safari browser compatibility issues - CURRENTLY FAILING
    
    When Safari users manually enter dates, registration fails due to
    date format incompatibility.
    
    These tests will FAIL until the bug is fixed!
    """
    
    @pytest.mark.xfail(reason="BUG: Safari slash format causes registration to fail", strict=True)
    def test_registration_fails_with_safari_slash_format(self):
        """
        CURRENTLY FAILS: Safari user with slash-formatted date gets rejected
        
        BUG FLOW:
        1. Safari user manually enters: "2024/06/15 14:30"
        2. EventService calls DateParser.parse_event_datetime()
        3. DateParser only accepts ISO format, raises DateParseError
        4. EventService converts to RegistrationError
        5. User sees error message and cannot register
        
        AFFECTED FILES:
        - src/date_parser.py, line 47-54 (root cause)
        - src/event_service.py, line 54-62 (propagates error)
        
        TRIGGER: Safari user submits form with manual date entry
        EXPECTED: Registration should succeed
        ACTUAL: RegistrationError is raised, registration fails
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
    
    @pytest.mark.xfail(reason="BUG: US date format with AM/PM causes registration to fail", strict=True)
    def test_registration_fails_with_us_date_format(self):
        """
        CURRENTLY FAILS: US-locale Safari user with MM/DD/YYYY format rejected
        
        BUG LOCATION: src/date_parser.py, parse_event_datetime method
        TRIGGER: User submits "06/15/2025 02:30 PM"
        EXPECTED: Successful registration
        ACTUAL: RegistrationError raised
        """
        service = EventService()
        
        # US format with AM/PM (common Safari manual entry)
        us_date = "06/15/2025 02:30 PM"
        
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
    Tests demonstrating Firefox browser compatibility issues - SHOULD FAIL
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
    
    @pytest.mark.xfail(reason="BUG: Text month format causes registration to fail", strict=True)
    def test_registration_fails_with_firefox_text_month(self):
        """
        CURRENTLY FAILS: Firefox user with text month format rejected
        
        BUG LOCATION: src/date_parser.py, line 47-54
        TRIGGER: User submits "Jun 15, 2025 14:30"
        EXPECTED: Successful registration
        ACTUAL: RegistrationError raised
        """
        service = EventService()
        
        # Text month format (common Firefox manual entry)
        firefox_date = "Jun 15, 2025 14:30"
        
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
