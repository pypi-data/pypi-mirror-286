#! /usr/bin/python3

# Brief WordX main program
# Author: Ashad Mohamed (aka. mashad)
# **********************************
# This the track changes implementation for this project, contain all general function
# to implement docx manipulation.

import json
import docx2python
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
    
# TO-DO: Function Tracking Modifications
def trackModifications(file_path: str) -> dict:
    return {}