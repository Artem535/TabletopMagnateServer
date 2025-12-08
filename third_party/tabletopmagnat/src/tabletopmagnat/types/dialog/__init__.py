"""
Dialog Package Initialization.

This module initializes the `dialog` package and re-exports the main `Dialog` class.
The `Dialog` class is used to manage sequences of messages in the TabletopMagnat application.

Exports:
    Dialog: A class for managing and organizing a conversation history as a list of message objects.
"""

from tabletopmagnat.types.dialog.dialog import Dialog

__all__ = ["Dialog"]