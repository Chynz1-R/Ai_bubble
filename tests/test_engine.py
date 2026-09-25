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

    def test_cybersecurity_prompt_uses_defense_language(self) -> None:
        analysis = AURELIAEngine().analyze("How can we reduce impersonation fraud in online support?")

        self.assertIn("detection", analysis.research_question.lower())
        self.assertTrue(any("security review" == item.lower() for item in analysis.human_approval_required))

    def test_generic_prompt_uses_generic_fallback(self) -> None:
        analysis = AURELIAEngine().analyze("How can we improve public trust in new research tools?")

        self.assertIn("Which measurable interventions could address this problem", analysis.research_question)
        self.assertTrue(any("domain expert review" in item.lower() for item in analysis.human_approval_required))

    def test_keyword_matching_avoids_partial_word_false_positive(self) -> None:
        analysis = AURELIAEngine().analyze("How can we improve seafood traceability?")

        self.assertIn("Which measurable interventions could address this problem", analysis.research_question)

    def test_hyphenated_phrase_matches_multiword_keyword(self) -> None:
        analysis = AURELIAEngine().analyze("How should we prepare for storm-surge damage?")

        self.assertIn("wetland", analysis.render().lower())

    def test_blank_problem_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AURELIAEngine().analyze("   ")

    def test_punctuation_only_problem_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            AURELIAEngine().analyze("...?!")


if __name__ == "__main__":
    unittest.main()
