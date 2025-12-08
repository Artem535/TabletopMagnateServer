from enum import StrEnum


class MessageRoles(StrEnum):
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    TOOL = "tool"
    DEVELOPER = "developer"
