import json
import docx2python
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# TO-DO: Function Get All Comments
def getcomments(file_path: str) -> []:
    comments = []
    with docx2python.docx2python(file_path) as docx_content:
        for comment in docx_content.comments:
            comments.append(comment)

        text, author, timestamp, comment = comment
        # Print or process each component as needed
        print(f"Text: {text.strip()}")
        print(f"Author: {author}")
        print(f"Timestamp: {timestamp}")
        print(f"Comment: {comment.strip()}\n")
