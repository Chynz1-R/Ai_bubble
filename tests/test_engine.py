import unittest

from aurelia.engine import AURELIAEngine


class AURELIAEngineTests(unittest.TestCase):
    def test_flooding_prompt_uses_structured_sections(self) -> None:
        analysis = AURELIAEngine().analyze("Coastal flooding is displacing communities.")

        rendered = analysis.render()

        self.assertIn("Research question:", rendered)
        self.assertIn("Evidence status:", rendered)
        self.assertIn("Known:", rendered)
        self.assertIn("Hypotheses:", rendered)
        self.assertIn("Uncertainty:", rendered)
        self.assertIn("Human approval required:", rendered)
        self.assertIn("wetland", rendered.lower())

    def test_blank_problem_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AURELIAEngine().analyze("   ")


if __name__ == "__main__":
    unittest.main()
