import os
from pathlib import Path

from doctag import TagIndex
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.validation import ValidationError, Validator


def get_ti():
    try:
        dtdb = Path(os.environ["DTDB"])
    except KeyError:
        dtdb = Path(Path.home(), ".dtdb.csv")
    try:
        ti = TagIndex.from_json(file_name=dtdb)
    except FileNotFoundError:
        print(f"Creating index at {dtdb}")
        ti = initialize(location=dtdb)
    return ti


class _NoFileValidator(Validator):
    def validate(self, document: Document):
        if os.path.isfile(document.text):
            raise ValidationError(message=f"File {document.text} already exists.")


def initialize(location: str):
    ti = TagIndex()
    ti.to_json(file_name=location)
    return ti
