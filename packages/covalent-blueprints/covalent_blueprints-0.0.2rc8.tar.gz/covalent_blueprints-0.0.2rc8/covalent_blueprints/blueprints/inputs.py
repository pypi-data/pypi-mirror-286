# Copyright 2024 Agnostiq Inc.
"""Arguments for Covalent blueprints."""
from typing import Tuple

from covalent_blueprints.reader.script import CovalentScript


class BlueprintInputs:
    """Provides arguments interface for Covalent blueprints."""

    def __init__(self, script: CovalentScript):
        self._args, self._kwargs = script.core_function_inputs
        if not isinstance(self._args, tuple):
            raise ValueError("Core function arguments must be a tuple")
        if not isinstance(self._kwargs, dict):
            raise ValueError("Core function keyword arguments must be a dict")

    @property
    def args(self) -> tuple:
        """Default arguments for the blueprint's core function."""
        return self._args

    @args.setter
    def args(self, value: tuple) -> None:
        if isinstance(value, tuple):
            self._args = value
        else:
            raise ValueError("args must be a tuple")

    @property
    def kwargs(self) -> dict:
        """Default keyword arguments for the blueprint's core function."""
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value: dict) -> None:
        if isinstance(value, dict):
            self._kwargs = value
        else:
            raise ValueError("kwargs must be a dict")

    def to_dict(self):
        """Return the arguments as a dictionary."""
        return {"args": self.args, "kwargs": self.kwargs}

    def override_defaults(self, args, kwargs) -> Tuple[tuple, dict]:
        """Override the default arguments with the provided args and kwargs."""

        new_args = list(self.args)
        for i, arg in enumerate(args):
            if i < len(new_args):
                new_args[i] = arg
            else:
                new_args.append(arg)

        new_kwargs = self.kwargs.copy()
        new_kwargs.update(**kwargs)

        return tuple(new_args), new_kwargs

    def __repr__(self):
        return f"BlueprintInputs(args={self.args}, kwargs={self.kwargs})"
