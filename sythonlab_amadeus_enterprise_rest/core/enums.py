from enum import Enum


class RequestMethod(Enum):
    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"


class Currency(Enum):
    USD = "USD"
    JMD = "JMD"


class TravelerType(Enum):
    ADULT = "ADULT"
    CHILD = "CHILD"
    INFANT = "HELD_INFANT"


class PaymentMethod(Enum):
    CASH = "CASH"


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class DocumentType(Enum):
    PASSPORT = "PASSPORT"
