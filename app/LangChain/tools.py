#!/bin/env python
# -*- coding: utf-8 -*-
import datetime
from datetime import date
from langchain.tools import tool

from deepagents.backends import FilesystemBackend

gFs = FilesystemBackend(root_dir='/', virtual_mode=False)


@tool
def current_date() -> str:
    """
    Gets the current date. You can use this tool to get results when the current date is included in the question. \
    For example: What is the date today?
    @param text: The input argument is an empty string
    @return: The output is always a character representation of the current date
    """
    return "toady's date is: " + str(date.today())


@tool
def current_date_time() -> str:
    """
    Gets the current date and time. You can use this tool to get results when the current date and time are included in the question. \
    For example: What time is it? What is the current time?
    @param text: The input argument is a blank string
    @return: The output should be represented as a string representing the current date plus the current time.
    """
    return "It's now is: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@tool
def delete_file(path: str) -> bool:
    """Delete a file from the filesystem.
    Args:
        path: file full path
    return: is deleted or not
    """
    print (f"You have deleted the file: {path} (NOT ^_^)")
    return False

@tool
def read_file(path: str) -> str:
    """Read a file from the filesystem.
    Args:
        path: file full path

    return: the file contents
    """
    return gFs.read(path)

