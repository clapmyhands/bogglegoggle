import sys, os
from flask import Flask

PROJECT_PATH = os.path.join(os.path.dirname(__file__), "..")
ASSET_PATH = os.path.join(os.path.dirname(__file__), "../asset")
DB_PATH = os.path.join(PROJECT_PATH,"boggle.db")