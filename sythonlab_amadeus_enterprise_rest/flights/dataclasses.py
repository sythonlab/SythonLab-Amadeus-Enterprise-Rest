#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: dataclasses.py
Author: Sython Lab (sythonlab@gmail.com)
Created: 2025-12-04
"""

from dataclasses import dataclass
from typing import Optional

from sythonlab_amadeus_enterprise_rest.core.enums import TravelerType, Gender, DocumentType, CardBrand


@dataclass
class SearchAvailabilityItinerary:
    """Dataclass for search availability itinerary."""

    id: str
    origin_location_code: str
    destination_location_code: str
    departure_date: str


@dataclass
class SearchAvailabilityPax:
    """Dataclass for search availability passenger."""

    id: str
    traveler_type: TravelerType


@dataclass
class ReservePax:
    """Dataclass for reserve passenger."""

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


@dataclass
class PaymentData:
    """Dataclass for card payment data."""

    brand: Optional[CardBrand] = None
    holder: Optional[str] = None
    number: Optional[str] = None
    expiry_date: Optional[str] = None
    security_code: Optional[str] = None
