#! /usr/bin/python3

# Brief WordX main program
# Author: Ashad Mohamed (aka. mashad)
# **********************************
# This the convert docx to json implementation for this project, contain all general function
# to implement docx manipulation.

import json
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn


def get_run_style(run):
    style = {
        'bold': run.bold,
        'italic': run.italic,
        'underline': run.underline,
        'color': run.font.color.rgb if run.font.color.rgb else None,
        'size': run.font.size.pt if run.font.size else None,
        'name': run.font.name,
    }
    return style

def get_paragraph_alignment(para):
    alignments = {
        WD_PARAGRAPH_ALIGNMENT.LEFT: 'left',
        WD_PARAGRAPH_ALIGNMENT.CENTER: 'center',
        WD_PARAGRAPH_ALIGNMENT.RIGHT: 'right',
        WD_PARAGRAPH_ALIGNMENT.JUSTIFY: 'justify'
    }
    return alignments.get(para.alignment, 'left')  # Default to 'left' if alignment is None

def read_word_file(file_path):
    doc = Document(file_path)
    data = []

    for para in doc.paragraphs:
        para_data = {
            'type': 'paragraph',
            'text': '',
            'runs': [],
            'alignment': get_paragraph_alignment(para)
        }
        for run in para.runs:
            run_data = {
                'text': run.text,
                'style': get_run_style(run)
            }
            para_data['text'] += run.text
            para_data['runs'].append(run_data)
        
        if para_data['text']:  # Ensure text is not empty before adding to data
            data.append(para_data)
    
    return data

def generate_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def convertDocxToJson(word, output):
    # Read the Word file and generate JSON
    data = read_word_file(word)
    if data:
        generate_json(data, output)
        print(f"Successfully saved content from {word} to {output}.")