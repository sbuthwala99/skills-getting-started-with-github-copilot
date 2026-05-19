import copy

from src import app as app_module


# Keep an immutable snapshot of the original in-memory activities
_ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


def _reset_activities_to_original():
    app_module.activities = copy.deepcopy(_ORIGINAL_ACTIVITIES)


def pytest_configure(config):
    # Ensure activities start in the original state when pytest starts
    _reset_activities_to_original()


import pytest


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities before and after each test to keep tests isolated."""
    _reset_activities_to_original()
    yield
    _reset_activities_to_original()
