"""
Module Contains base validator implementation.
"""
from abc import ABC, abstractmethod
from typing import Self
from . import SerializerError


# Abstracted Validator Class
class BaseValidator(ABC):
    """
    Base Validation class that utilizes `SerializerError` from package as it's default raise_exception
    """

    def __init__(self: Self, raise_exception: SerializerError = SerializerError):
        self.raise_exception: SerializerError = raise_exception

    @abstractmethod
    def validate(self, data):
        pass
