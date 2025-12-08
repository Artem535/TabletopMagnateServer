"""
Dialog Class Module.

This module provides a `Dialog` class to manage and organize a sequence of messages
in the TabletopMagnat application. It allows for adding messages and converting them
into a list of dictionaries, suitable for external processing or API interaction.

Classes:
    Dialog: A container for managing a sequence of message objects.
"""
from pydantic import BaseModel, Field

from tabletopmagnat.types.messages import UserMessage
from tabletopmagnat.types.messages.base_message import BaseMessage


class Dialog(BaseModel):
    """
    A class representing a sequence of messages in a conversation.

    Attributes:
        messages (list[BaseMessage]): A list of message objects in the dialog.

    Methods:
        add_message(message): Adds a message to the dialog if it is an instance of BaseMessage.
        to_list(): Converts all messages in the dialog into a list of dictionaries.
    """

    messages: list[BaseMessage] | None = Field(
        default=None,
        examples=[[UserMessage(content="Hello, how are you?")]],
        description="List of messages in the dialog"
    )

    def add_message(self, message: BaseMessage) -> None:
        """
        Adds a message to the dialog.

        Args:
            message (BaseMessage): The message to be added.

        Raises:
            TypeError: If the provided message is not an instance of BaseMessage.
        """
        if self.messages is None:
            self.messages = []

        if isinstance(message, BaseMessage):
            self.messages.append(message)
        else:
            raise TypeError("Message must be an instance of BaseMessage")

    def to_list(self) -> list[dict]:
        """
        Converts each message in the dialog into a dictionary format.

        Returns:
            list[dict]: A list of dictionaries, each representing a message with 'role' and 'content' keys.
        """
        return [message.to_dict() for message in self.messages] if self.messages else []

    def __iadd__(self, other):
        if isinstance(other, Dialog):
            self.messages.extend(other.messages)
            return self

        raise TypeError(f"Cannot add {type(other)} to Dialog")

    def get_last_message(self):
        return self.messages[-1] if self.messages and len(self.messages) else None

    def pop_last_message(self):
        return self.messages.pop() if self.messages and len(self.messages) else None

    def replace_last_message(self, message: BaseMessage):
        if self.messages:
            self.messages[-1] = message
        else:
            self.messages = [message]

        return None
