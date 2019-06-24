import os
from pathlib import Path

from doctag import FileTagIndex
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.validation import ValidationError, Validator


def get_ti_file():
    try:
        dtdb = Path(os.environ["DOCTAG_DB"])
    except KeyError:
        dtdb = Path(Path.home(), ".dtdb.json")
    return dtdb


def get_ti():
    ti = FileTagIndex.from_json(at=get_ti_file())
    return ti


def doc_str(ti: FileTagIndex, tag: str) -> str:
    doc_str = ", ".join(sorted(ti.tag_to_docs[tag]))
    return doc_str


def tag_str(ti: FileTagIndex, doc: str) -> str:
    tag_str = ", ".join(sorted(ti.doc_to_tags[doc]))
    return tag_str


class _NoFileValidator(Validator):
    def validate(self, document: Document):
        if os.path.isfile(document.text):
            raise ValidationError(message=f"File {document.text} already exists.")


def initialize(at: str):
    try:
        root_dir = Path(os.environ["DTROOT"])
    except KeyError:
        root_dir = Path.home()
    ti = FileTagIndex(root_dir=str(root_dir), at=at)
    ti.to_json()
    return ti
