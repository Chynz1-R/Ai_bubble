import subprocess
import sys
import unittest


class CLITests(unittest.TestCase):
    def test_module_invocation_outputs_expected_sections(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "aurelia", "How effective is intervention for coastal flooding?"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("Problem:", result.stdout)
        self.assertIn("Research question:", result.stdout)
        self.assertIn("Human approval required:", result.stdout)

    def test_module_invocation_requires_problem_argument(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "aurelia"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage:", result.stderr.lower())
        self.assertIn("problem", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
