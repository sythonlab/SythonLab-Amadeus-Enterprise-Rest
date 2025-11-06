from enum import Enum


class RequestMethod(Enum):
    """Represents HTTP request methods."""

    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"


class Currency(Enum):
    """Represents different currency codes."""

    USD = "USD"
    JMD = "JMD"


class TravelerType(Enum):
    """Represents different types of travelers."""

    ADULT = "ADULT"
    CHILD = "CHILD"
    INFANT = "HELD_INFANT"


class PaymentMethod(Enum):
    """Represents different payment methods."""

    CASH = "CASH"


class Gender(Enum):
    """Represents gender"""
    MALE = "MALE"
    FEMALE = "FEMALE"


class DocumentType(Enum):
    """Represents different document types."""
    
    PASSPORT = "PASSPORT"
