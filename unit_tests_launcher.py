#!/usr/bin/env python3
'''
This script is used to launch the unit tests.
There are two ways to run the unit tests:
1. Run the unit tests from the command line:
```
$ pipenv run python unit_tests_launcher.py
```
2. Run the unit tests from the GitHub action workflow: unitest-workflow.yml

Configurations:
`COVERAGE_THRESHOLD`: [int] The minimum coverage threshold.
`DIRS_TO_EVALUATE`: [list[str]] The directories to evaluate for unit tests.
`TEST_CASES_FOLDER`: [str] The folder where the test cases are located.
'''

import sys
import pytest
import xml.etree.ElementTree as ET

COVERAGE_THRESHOLD = 35
DIRS_TO_EVALUATE = [
    "src/connector/",
    "src/services/",
    "src/controllers/",
    "src/utils/",
    ]

TEST_CASES_FOLDER = "tests/"

def check_coverage(threshold, result):
    """
    Check the coverage of the code based on the given threshold.

    Parameters:
        threshold (float): The minimum coverage threshold.
        result (int): The result of the unit tests.

    Returns:
        None

    Raises:
        Exception: If the unit tests fail.

    This function parses the coverage.xml file to get the coverage percentage.
    It prints the coverage percentage and checks if it meets the threshold.
    If the coverage is below the threshold, it prints a message and exits with a status code of 1.
    If the coverage meets the threshold, it prints a success message.
    If the result is not 0, it raises an exception indicating that the unit tests failed.
    If the coverage.xml file cannot be parsed or is not found, it prints an error message and exits with a status code of 1.
    """
    in_red = '\033[91m'
    in_green = '\033[92m'
    in_yellow = '\033[93m'
    reset = '\033[0m'
    printing = lambda color, message: print(f"{color}{message}{reset}")

    try:
        tree = ET.parse('coverage.xml')
        root = tree.getroot()
        coverage = float(root.get('line-rate')) * 100 # type: ignore

        print(f"Coverage: {coverage:.2f}%")

        if coverage < threshold:
            printing(in_red,f"✋ Coverage is below threshold. Expected at least {threshold}%, but got {coverage:.2f}% ✋")
            sys.exit(1)
        else:
            printing(in_green, f"▶️ Coverage meets the threshold: {coverage:.2f}% >= {threshold}%")
        if result != 0:
            printing(in_red, '🚫 Unit tests failed, check the "FAILURES" section 🚫')
            raise Exception(f"Unit tests failed. See coverage.xml for details")
        else:
            printing(in_green, 'All unit tests passed 🚀')
    except ET.ParseError:
        printing(in_red, "🚫 Failed to parse coverage XML report 🚫")
        sys.exit(1)
    except FileNotFoundError:
        printing(in_red, "🚫 Coverage XML report not found 🚫")
        sys.exit(1)

params = [
        *[f"--cov={path}" for path in DIRS_TO_EVALUATE],
        "--cov-report=xml:coverage.xml",
        TEST_CASES_FOLDER,
    ]

print(params)
# ▶️ generate the XML report:
result = pytest.main(params)
check_coverage(COVERAGE_THRESHOLD, result)
