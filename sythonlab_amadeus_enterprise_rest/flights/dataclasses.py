from dataclasses import dataclass

from sythonlab_amadeus_enterprise_rest.core.enums import TravelerType, Gender, DocumentType


@dataclass
class SearchAvailabilityItinerary:
    id: str
    origin_location_code: str
    destination_location_code: str
    departure_date: str


@dataclass
class SearchAvailabilityPax:
    id: str
    traveler_type: TravelerType


@dataclass
class ReservePax:
    id: str
    date_of_birth: str
    first_name: str
    last_name: str
    gender: Gender
    email: str
    phone_country_code: str
    phone_number: str
    document_type: DocumentType
    document_number: str
    document_issuance_date: str
    document_expiry_date: str
    document_issuance_country_code: str
    nationality_code: str
