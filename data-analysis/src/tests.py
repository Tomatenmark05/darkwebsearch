import unittest
from ai_client import safe_parse_json

class TestAIClient(unittest.TestCase):
    def test_safe_parse_json_valid(self):
        json_str = '{"tags": ["tag1", "tag2"], "title": "Test Title", "legality": true}'
        result = safe_parse_json(json_str)
        self.assertEqual(result["tags"], ["tag1", "tag2"])
        self.assertEqual(result["title"], "Test Title")
        self.assertTrue(result["legality"])

    def test_safe_parse_json_invalid(self):
        # Missing closing brace, not valid JSON - should raise
        json_str = '{"tags": ["tag1", "tag2"], "title": "Test Title", "legality": true'
        with self.assertRaises(ValueError):
            safe_parse_json(json_str)
        # Input lacking any valid JSON object at all
        with self.assertRaises(ValueError):
            safe_parse_json('just plain text')

    def test_safe_parse_json_non_dict(self):
        # Returns valid object that's not dict (should be allowed, but content is arbitrary)
        json_str = '["not", "a", "dict"]'
        result = safe_parse_json(json_str)
        self.assertEqual(result, ["not", "a", "dict"])
        # Empty string should raise ValueError
        with self.assertRaises(ValueError):
            safe_parse_json('')

if __name__ == '__main__':
    unittest.main()
