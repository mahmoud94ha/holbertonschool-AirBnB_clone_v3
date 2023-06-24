#!/usr/bin/python3
"""
Contains the api app.py
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views import index
