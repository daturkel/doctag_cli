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
        dtdb = Path(Path.home(), ".dtdb.json")
    try:
        ti = TagIndex.from_json(file_name=dtdb)
    except FileNotFoundError:
        print(f"Tag index created at.")
        ti = initialize(location=dtdb)
    return TIFile.from_json(file_name=dtdb)


def doc_str(ti: TagIndex, tag: str) -> str:
    doc_str = ", ".join(sorted(ti.tag_to_docs[tag]))
    return doc_str


def tag_str(ti: TagIndex, doc: str) -> str:
    tag_str = ", ".join(sorted(ti.doc_to_tags[doc]))
    return tag_str


class _NoFileValidator(Validator):
    def validate(self, document: Document):
        if os.path.isfile(document.text):
            raise ValidationError(message=f"File {document.text} already exists.")


def _initialize(location: str):
    ti = TagIndex()
    ti.to_json(file_name=location)
    return ti


class TIFile(TagIndex):
    def __init__(self, loc):
        self.loc = loc
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.to_json(file_name=self.loc)

    @classmethod
    def from_json(cls, file_name: str):
        ti = TIFile(loc=file_name)
        ti_copy = super().from_json(file_name=file_name)
        ti.tag_to_docs = ti_copy.tag_to_docs
        ti.doc_to_tags = ti_copy.doc_to_tags
        return ti
