"""
Tests for EventService module (Fixed)

These tests verify that registration works when various date formats are provided.
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
    Tests demonstrating Safari browser compatibility issues - SHOULD PASS AFTER FIX
    """
    
    def test_registration_with_safari_slash_format(self):
        """
        Safari user with slash-formatted date should succeed
        """
        service = EventService()
        
        # Safari user manually enters date with slashes (30 days in future)
        future_date = (datetime.now() + timedelta(days=30))
        safari_date = future_date.strftime("%Y/%m/%d %H:%M")
        
        result = service.register_participant(
            name="Safari User",
            email="safari@example.com",
            event_datetime=safari_date
        )
        
        assert result["success"] is True
        assert "Safari User" in result["message"]
        assert service.get_registration_count() == 1
    
    def test_registration_with_us_date_format(self):
        """
        US-locale Safari user with MM/DD/YYYY format should succeed
        """
        service = EventService()
        
        # US format with AM/PM (common Safari manual entry)
        us_date = (datetime.now() + timedelta(days=30)).strftime("%m/%d/%Y %I:%M %p")
        
        result = service.register_participant(
            name="US User",
            email="us@example.com",
            event_datetime=us_date
        )
        
        assert result["success"] is True
        assert service.get_registration_count() == 1


class TestEventServiceFirefoxBrowserIssues:
    """
    Tests demonstrating Firefox browser compatibility issues - SHOULD PASS AFTER FIX
    """
    
    def test_registration_with_firefox_text_month(self):
        """
        Firefox user with text month format should succeed
        """
        service = EventService()
        
        # Text month format (common Firefox manual entry)
        firefox_date = (datetime.now() + timedelta(days=30)).strftime("%b %d, %Y %H:%M")
        
        result = service.register_participant(
            name="Firefox User",
            email="firefox@example.com",
            event_datetime=firefox_date
        )
        
        assert result["success"] is True
        assert service.get_registration_count() == 1
        
    def test_registration_fails_for_past_date(self):
        service = EventService()
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
