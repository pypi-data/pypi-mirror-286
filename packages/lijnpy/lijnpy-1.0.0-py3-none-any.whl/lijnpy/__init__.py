import logging
import os

API_KEY = os.environ.get("DELIJN_API_KEY", "NO_API_KEY")
_logger = logging.getLogger(__name__)
