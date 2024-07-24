"""Utility functions for the PT42 wrapper."""

import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder for datetime objects."""

    def default(self, obj):
        """Encodes datetime objects to ISO format."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
