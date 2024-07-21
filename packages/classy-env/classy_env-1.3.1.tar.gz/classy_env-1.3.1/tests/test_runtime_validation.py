import pytest

from classyenv import ClassyEnv, EnvVar, errors


def test_runtime_validation_env_vars_not_defined():
    with pytest.raises(errors.EnvVarsNotFoundError) as e:

        class NotPresentSettings(ClassyEnv, runtime_check=True):
            test_env1 = EnvVar("TEST1")
            test_env2 = EnvVar("TEST2")

    assert (
        "Couldn't find the following environment variables:\n\t'TEST1'\n\t'TEST2'"
        == e.value.args[0]
    )


def test_runtime_validation_repeated_env_vars():
    with pytest.raises(errors.RepeatedEnvVarsError) as e:

        class DoubledSettings(ClassyEnv, runtime_check=True):
            foo = EnvVar("FOO")
            bar = EnvVar("FOO")

    assert (
        "The following environment variables were declared more than once:\n\t'FOO'"
        == e.value.args[0]
    )


def test_runtime_validation_env_vars_not_defined_and_repeated_env_vars():
    with pytest.raises(ExceptionGroup) as e:

        class NotPresentAndDoubledSettings(ClassyEnv, runtime_check=True):
            test_env1 = EnvVar("TEST1")
            test_env2 = EnvVar("TEST2")
            test_env3 = EnvVar("TEST1")
            test_env4 = EnvVar("TEST2")

    assert (
        "The following errors occurred while trying to instantiate object of the 'NotPresentAndDoubledSettings' class:"
        == e.value.args[0]
    )
