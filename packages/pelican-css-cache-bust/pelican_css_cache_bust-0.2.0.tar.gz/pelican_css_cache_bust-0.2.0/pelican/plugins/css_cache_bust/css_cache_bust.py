"""Pelican plugin to attach a unique string to the main CSS file.

Appends a query string to make sure CSS files are "versioned".
"""

import hashlib
import logging
import os

from pelican import Pelican, signals


logger = logging.getLogger(__name__)


def _get_css_file_hash(
    theme_path: str, static_paths: list, css_file: str
) -> str:
    """Calculate a short hash for a file."""
    found_file = None

    theme_paths = list(
        os.path.join(theme_path, p, css_file) for p in static_paths
    )
    for p in theme_paths:
        found_file = p if os.path.isfile(p) else found_file

    if found_file is None:
        logger.error(
            'Could not find CSS_FILE "%s" '
            'in "THEME_STATIC_PATHS" locations: %s',
            css_file,
            theme_paths,
        )
        return ""
    else:
        with open(found_file, "rb") as f:
            digest = hashlib.file_digest(f, "md5").hexdigest()

        return digest[:6]


def create_css_cache_bust(pelican: Pelican) -> None:
    """Set the value of CSS_FILE_CACHE_BUST."""
    current = pelican.settings.get("CSS_FILE_CACHE_BUST")
    if current is not None:
        return None

    cache_string = _get_css_file_hash(
        pelican.settings.get("THEME"),
        pelican.settings.get("THEME_STATIC_PATHS"),
        pelican.settings.get("CSS_FILE"),
    )
    cache_string = f"?{cache_string}"

    logger.debug('Setting CSS_FILE_CACHE_BUST: "%s"', cache_string)
    pelican.settings["CSS_FILE_CACHE_BUST"] = cache_string


def register() -> None:
    """Register Pelican plugin."""
    signals.initialized.connect(create_css_cache_bust)
