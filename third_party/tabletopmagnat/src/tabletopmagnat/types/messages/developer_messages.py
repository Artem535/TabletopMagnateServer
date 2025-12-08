"""
Message Types Module.

This module provides classes representing different message types used in the TabletopMagnat application.
Each class inherits from `BaseMessage` and defines a specific role (User, Assistant, System).
The classes also include a method to convert the message to a dictionary format suitable for external APIs.

**Note**: The `Developer` message type is used exclusively in the GPT-OSS version of the application for internal developer-specific instructions or context.
It is not part of the standard message schema and is ignored or unsupported in other versions.

Classes:
    Developer: Represents a developer-level message used for internal instructions or context in GPT-OSS.
"""
from typing import override

from tabletopmagnat.types.messages.base_message import BaseMessage
from tabletopmagnat.types.messages.message_roles import MessageRoles


class DeveloperMessage(BaseMessage):
    """
    A message class for developer-level instructions or context in GPT-OSS.

    This message type is only recognized and processed in the GPT-OSS version of the application.
    It allows sending internal developer-specific directives that influence behavior during development or debugging.
    In production or other versions, this role may be ignored or treated as an unknown role.

    Attributes:
        role (MessageRoles): The role of the message sender, fixed to `MessageRoles.DEVELOPER`.

    Methods:
        to_dict(): Converts the message into a dictionary with 'role' and 'content' keys.
    """

    role: MessageRoles = MessageRoles.DEVELOPER

    @override
    def to_dict(self):
        """
        Converts the message into a dictionary format.

        Returns:
            dict: A dictionary with 'role' and 'content' keys, where role is stringified using its value.
        """
        return {"role": str(self.role.value), "content": self.content}