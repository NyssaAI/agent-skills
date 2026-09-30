import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from assemble import canonical_hash_content  # noqa: E402


class AssemblyTests(unittest.TestCase):
    def test_generated_provenance_hash_is_stable_across_line_endings(self):
        lf = canonical_hash_content(b"one\ntwo\n")
        crlf = canonical_hash_content(b"one\r\ntwo\r\n")
        cr = canonical_hash_content(b"one\rtwo\r")
        self.assertEqual(lf, crlf)
        self.assertEqual(lf, cr)


if __name__ == "__main__":
    unittest.main()
