import unittest

from mesh.secrets_scan import scan_text


class TestSecretsScan(unittest.TestCase):
    def test_flags_hex32(self) -> None:
        # Deliberate fake key material for scanner unit test only.
        fake = "deadbeefcafebabe0123456789abcdef"
        findings = scan_text(f"app key {fake}")
        kinds = {f["kind"] for f in findings}
        self.assertIn("hex32", kinds)

    def test_allowlist_placeholder(self) -> None:
        text = "LORAWAN_APPKEY=YOUR_APP_KEY_HERE"
        self.assertEqual(scan_text(text), [])

    def test_pem(self) -> None:
        text = "-----BEGIN RSA PRIVATE KEY-----\nMII\n-----END RSA PRIVATE KEY-----"
        findings = scan_text(text)
        self.assertTrue(any(f["kind"] == "pem_private_key" for f in findings))


if __name__ == "__main__":
    unittest.main()
