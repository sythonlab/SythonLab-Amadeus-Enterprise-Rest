#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: dataclasses.py
Author: Sython Lab (sythonlab@gmail.com)
Created: 2026-05-28
"""

from dataclasses import dataclass


@dataclass
class AmadeusConfig:
    """Dataclass Amadeus config."""

    client_id: str
    client_secret: str
    production: bool
    api_url: str
