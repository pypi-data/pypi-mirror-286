from pytest import fixture
from ..core_utils import set_conf


@fixture
def tecton_unit_test():
    with set_conf(
        {"TECTON_DEBUG": "true", "TECTON_FORCE_FUNCTION_SERIALIZATION": "false"}
    ):
        yield
