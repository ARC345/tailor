"""
Pytest configuration for Tailor sidecar tests.

This module configures pytest for testing the refactored codebase.
"""

import sys
from pathlib import Path

# Add sidecar to path for imports
sidecar_path = Path(__file__).parent.parent
sys.path.insert(0, str(sidecar_path))


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
