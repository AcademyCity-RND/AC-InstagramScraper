"""Test that the Axiom route is properly registered in the microservice routes."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def test_axiom_route_registered():
    """Verify that /axiom/comments endpoint is in the registered endpoints."""
    try:
        from routes import ENDPOINTS
    except ImportError:
        pytest.skip("bottle not installed in current environment")

    paths = [p for p, _ in ENDPOINTS]
    assert "/axiom/comments" in paths
