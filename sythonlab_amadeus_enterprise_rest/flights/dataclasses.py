from dataclasses import dataclass

from sythonlab_amadeus_enterprise_rest.core.enums import TravelerType


@dataclass
class SearchAvailabilityItinerary:
    id: str
    originLocationCode: str
    destinationLocationCode: str
    departureDateTimeRange: str


@dataclass
class SearchAvailabilityPax:
    id: str
    travelerType: TravelerType
