"""
Event Registration Service

Handles event registration business logic including participant registration
and date/time validation.
"""

from datetime import datetime
from typing import Dict, List, Optional
from .date_parser import DateParser, DateParseError


class RegistrationError(Exception):
    """Raised when registration fails"""
    pass


class EventService:
    """Service for managing event registrations"""

    def __init__(self):
        self.registrations: List[Dict] = []
        self.date_parser = DateParser()

    def register_participant(
        self,
        name: str,
        email: str,
        event_datetime: str,
        event_name: str = "Tech Conference 2024"
    ) -> Dict:
        """
        Register a participant for an event.

        Args:
            name: Participant name
            email: Participant email
            event_datetime: Event date/time as string from browser form
            event_name: Name of the event

        Returns:
            Registration confirmation dict

        Raises:
            RegistrationError: If registration fails due to validation errors
        """
        # Validate required fields
        if not name or not email:
            raise RegistrationError("Name and email are required")

        # Parse the event datetime
        try:
            parsed_datetime = self.date_parser.parse_event_datetime(event_datetime)
        except DateParseError as e:
            raise RegistrationError(
                f"Failed to register: {str(e)}. "
                f"Please use format YYYY-MM-DDTHH:MM"
            ) from e

        # Validate event is in the future
        if parsed_datetime < datetime.now():
            raise RegistrationError("Cannot register for past events")

        # Create registration record
        registration = {
            "name": name,
            "email": email,
            "event_name": event_name,
            "event_datetime": parsed_datetime.isoformat(),
            "registered_at": datetime.now().isoformat(),
            "status": "confirmed"
        }

        self.registrations.append(registration)

        return {
            "success": True,
            "registration_id": len(self.registrations),
            "message": f"Successfully registered {name} for {event_name}",
            "event_date": self.date_parser.format_for_display(parsed_datetime)
        }

    def get_registrations(self) -> List[Dict]:
        """Get all registrations"""
        return self.registrations.copy()

    def get_registration_count(self) -> int:
        """Get total number of registrations"""
        return len(self.registrations)
