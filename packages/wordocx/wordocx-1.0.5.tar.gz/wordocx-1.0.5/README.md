# wordocx

A simple DOCX manipulation utility library.

## Installation

```sh
pip install wordocx
```

## Usage

```python
from wordocx import getComments, convertDocxToJson, convertJsonToDocx

# Example usage to get comments
comments = getComments('example.docx')


# Read the Word file and generate JSON
convertDocxToJson('example.docx', outputFile)

# Read the JSON file and generate DOCX
convertJsonToDocx('example.json', outputFile)
```

**requirements.txt**
```makefile
python-docx>=0.8.10
docx2python>=1.27.0
jsonlib-python3>=1.6.1
```
