import sys

import pytest
from pytest_bdd import scenarios
from tests.e2e.conftest import TEST_HARNESS_PATH


@pytest.fixture(autouse=True, scope="module")
def setup(request):
    pass


if sys.version_info >= (3, 9):
    scenarios(
        f"{TEST_HARNESS_PATH}/gherkin/config.feature",
    )
