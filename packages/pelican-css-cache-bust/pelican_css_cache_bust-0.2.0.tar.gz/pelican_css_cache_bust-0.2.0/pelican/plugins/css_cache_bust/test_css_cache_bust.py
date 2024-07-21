import hashlib
import os
import random
from tempfile import NamedTemporaryFile, TemporaryDirectory
import unittest

from .css_cache_bust import _get_css_file_hash, create_css_cache_bust


class TestCssCacheBust(unittest.TestCase):
    def setUp(self):
        self.tmp_theme_dir = TemporaryDirectory(delete=False)

        # Create some directories under the theme dir to test searching
        # in static paths
        parent = self.tmp_theme_dir.name
        self.tmp_static_paths = [
            TemporaryDirectory(dir=parent, delete=False),
            TemporaryDirectory(dir=parent, delete=False),
            TemporaryDirectory(dir=parent, delete=False),
        ]

        # Put the CSS file in a random choice of the static_paths
        # directory
        parent = random.choice(self.tmp_static_paths).name
        self.tmp_css_file = NamedTemporaryFile(
            dir=parent,
            delete=False,
            mode="w",
        )
        self.tmp_css_file.write("body { color: inherit }")
        self.tmp_css_file.close()

        # Convenience arguments
        self.theme_path = self.tmp_theme_dir.name
        self.static_paths = [
            os.path.basename(d.name) for d in self.tmp_static_paths
        ]
        self.css_file = os.path.basename(self.tmp_css_file.name)

    def test_hash_as_expected(self):
        """Test that hashing changes after file change."""
        expected_hash = ""
        with open(self.tmp_css_file.name, "rb") as f:
            digest = hashlib.file_digest(f, "md5").hexdigest()
            expected_hash = digest[:6]

        ret = _get_css_file_hash(
            self.theme_path, self.static_paths, self.css_file
        )
        self.assertEqual(expected_hash, ret)

        with open(self.tmp_css_file.name, "w") as f:
            f.write("body { color: transparent }")

        ret = _get_css_file_hash(
            self.theme_path, self.static_paths, self.css_file
        )
        self.assertNotEqual(expected_hash, ret)

    def test_hash_missing_file(self):
        """Test that a not existing file fails."""
        ret = _get_css_file_hash(
            self.theme_path, self.static_paths, "no-file"
        )
        self.assertEqual("", ret)

    def test_set_pelican_settings(self):
        """Test if we set CSS_FILE_CACHE_BUST correctly."""

        class _MockPelican:
            settings = {
                "THEME": self.theme_path,
                "THEME_STATIC_PATHS": self.static_paths,
                "CSS_FILE": self.css_file,
            }

        mock_pelican = _MockPelican()
        expected_hash = ""
        with open(self.tmp_css_file.name, "rb") as f:
            digest = hashlib.file_digest(f, "md5").hexdigest()
            expected_hash = digest[:6]

        create_css_cache_bust(mock_pelican)

        self.assertEqual(
            f"?{expected_hash}",
            mock_pelican.settings.get("CSS_FILE_CACHE_BUST"),
        )

        mock_pelican.settings["CSS_FILE_CACHE_BUST"] = "do-nothing"
        create_css_cache_bust(mock_pelican)

        self.assertEqual(
            "do-nothing",
            mock_pelican.settings.get("CSS_FILE_CACHE_BUST"),
        )

    def tearDown(self):
        os.remove(self.tmp_css_file.name)

        for d in self.tmp_static_paths:
            d.cleanup()

        self.tmp_theme_dir.cleanup()
