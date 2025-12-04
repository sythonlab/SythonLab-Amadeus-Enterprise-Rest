#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: settings.py
Author: Sython Lab (sythonlab@gmail.com)
Created: 2025-12-04
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

AMADEUS_CONFIG = {
    "API_URL": os.getenv("AMADEUS_API_URL"),
    "CLIENT_ID": os.getenv("AMADEUS_CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("AMADEUS_CLIENT_SECRET"),
    "PRODUCTION": bool(int(os.getenv("PRODUCTION", "0"))),
}

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
