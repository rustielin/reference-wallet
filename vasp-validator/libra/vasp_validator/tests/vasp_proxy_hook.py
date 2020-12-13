from pytest import hookspec

from ..vasp_proxy import VaspProxy


@hookspec(firstresult=True)
def pytest_create_vasp_proxy() -> VaspProxy:
    """
    Controls which testee VASP object will be used during the tests
    """
