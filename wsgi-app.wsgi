#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/ubuntu/projeto-redes-2023-2")

from app import app as application
