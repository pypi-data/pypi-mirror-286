import os

import pytest

from classyenv import ClassyEnv, EnvVar, errors

ENVVAR_01 = "0"
ENVVAR_02 = "1"
ENVVAR_03 = "YES"
ENVVAR_04 = "NO"
ENVVAR_05 = "1,2,3,4,5"
ENVVAR_06 = "3306"
ENVVAR_07 = "120.25"


os.environ["ENVVAR_01"] = ENVVAR_01
os.environ["ENVVAR_02"] = ENVVAR_02
os.environ["ENVVAR_03"] = ENVVAR_03
os.environ["ENVVAR_04"] = ENVVAR_04
os.environ["ENVVAR_05"] = ENVVAR_05
os.environ["ENVVAR_06"] = ENVVAR_06
os.environ["ENVVAR_07"] = ENVVAR_07


def one_zero_to_bool(val: str) -> bool:
    return bool(int(val))


def yes_no_to_bool(val: str) -> bool:
    return {
        "YES": True,
        "NO": False,
    }[val]


def comma_separated_to_list(val: str) -> list[int]:
    return [int(x) for x in val.split(",")]


class Settings(ClassyEnv):
    env_01 = EnvVar("ENVVAR_01", converter=one_zero_to_bool)
    env_02 = EnvVar("ENVVAR_02", converter=one_zero_to_bool)
    env_03 = EnvVar("ENVVAR_03", converter=yes_no_to_bool)
    env_04 = EnvVar("ENVVAR_04", converter=yes_no_to_bool)
    env_05 = EnvVar("ENVVAR_05", converter=comma_separated_to_list)
    env_06 = EnvVar("ENVVAR_06", converter=int)
    env_07 = EnvVar("ENVVAR_07", converter=float)


@pytest.mark.parametrize(
    ("converter", "value", "attr_name", "expected"),
    (
        (one_zero_to_bool, ENVVAR_01, "env_01", False),
        (one_zero_to_bool, ENVVAR_02, "env_02", True),
        (yes_no_to_bool, ENVVAR_03, "env_03", True),
        (yes_no_to_bool, ENVVAR_04, "env_04", False),
        (comma_separated_to_list, ENVVAR_05, "env_05", [1, 2, 3, 4, 5]),
        (int, ENVVAR_06, "env_06", 3306),
        (float, ENVVAR_07, "env_07", 120.25),
    ),
)
def test_converter_works(converter, value, attr_name, expected):
    obj = Settings()
    assert converter(value) == getattr(obj, attr_name)
    assert getattr(obj, attr_name) == expected


def test_cant_provide_non_callable():
    with pytest.raises(errors.NonCallableConverterError) as e:
        EnvVar("test", converter=120)  # type: ignore

    assert "Provided converter is not callable" == e.value.args[0]
