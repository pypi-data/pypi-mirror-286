import os

import pytest

from classyenv import ClassyEnv, EnvVar

os.environ["TEST_01"] = "test_01"


class Settings(ClassyEnv):
    env_01 = EnvVar("TEST_01", default="default_01")
    env_02 = EnvVar("TEST_02", default="default_02")
    env_03 = EnvVar("TEST_03", default="default_03", converter=lambda x: "converted")
    env_04 = EnvVar("TEST_04", default=None)


@pytest.fixture(name="obj")
def obj_fixture():
    yield Settings()


def test_default_when_envvar_is_defined(obj: Settings):
    assert obj.env_01 == "test_01"


def test_default_when_envvar_is_not_defined(obj: Settings):
    assert obj.env_02 == "default_02"


def test_converter_does_not_affect_default(obj: Settings):
    assert obj.env_03 != "converted"
    assert obj.env_03 == "default_03"


def test_can_set_none_as_default(obj: Settings):
    assert obj.env_04 is None
