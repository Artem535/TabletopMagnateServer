"""
Base Message Class Module.

This module defines the abstract base class for all message types in the TabletopMagnat application.
It serves as a template for user, assistant, and system messages, ensuring a consistent interface
and structure across different message implementations.

Classes:
    BaseMessage: Abstract base class that provides the foundation for message objects.
"""

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class BaseMessage(BaseModel, ABC):
    """
    Abstract base class for message objects.

    Attributes:
        content (str): The main content or text of the message.

    Methods:
        to_dict(): Abstract method that must be implemented by subclasses to return
                   a dictionary representation of the message.
    """

    content: str
    metadata: dict | None = Field(default=None, exclude=True)

    @abstractmethod
    def to_dict(self):
        """
        Converts the message into a dictionary format.

        This is an abstract method and must be implemented by subclasses.

        Returns:
            dict: A dictionary representation of the message with 'role' and 'content' keys.
        """
        raise NotImplementedError()
