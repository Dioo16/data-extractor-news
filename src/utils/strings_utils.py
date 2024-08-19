"""
Utility module for formatting strings to be used as filenames.

This module provides functions for converting strings into valid filenames by replacing disallowed
characters with underscores and ensuring the filename does not contain spaces.

Functions:
- format_to_allowed_filename: Formats a string to replace disallowed characters and spaces
  with underscores for use as a valid filename.
"""
import re

def format_to_allowed_filename(string: str) -> str:
    """
    Formats a string to be used as a valid filename by replacing disallowed characters.

    This function replaces any character that is not an alphanumeric character or a space with an
    underscore (`_`). It also replaces spaces with underscores to ensure the filename is valid and
    does not contain spaces.

    Args:
        string (str): The string to be formatted.

    Returns:
        str: The formatted string with disallowed characters replaced by underscores.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '_', string).replace(' ', '_')
