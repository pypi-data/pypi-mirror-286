"""
Unit tests for the package using pytest.

REF: <https://docs.pytest.org/en/7.4.x/>
"""


def test_imports():
    """Test that the package and a submodule can be imported."""

    import gpt2_prot  # pylint: disable=import-outside-toplevel

    assert gpt2_prot

    import gpt2_prot.scripts  # pylint: disable=import-outside-toplevel

    assert gpt2_prot.scripts
