"""Classy Env is a lightweight python package for managing environment variables in OOP way."""

from .base_class import ClassyEnv
from .descriptor import EnvVar

__version__ = "1.3.1"

__all__ = ["EnvVar", "ClassyEnv"]
