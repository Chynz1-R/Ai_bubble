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


if __name__ == "__main__":
    unittest.main()
