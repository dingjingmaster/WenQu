#!/bin/env python
# -*- coding: utf-8 -*-
from langchain.tools import tool


@tool
def search(keyword: list)->str:
    """Delete a file from the filesystem.
    Args:
        path: file full path
    return: is deleted or not
    """
    pass