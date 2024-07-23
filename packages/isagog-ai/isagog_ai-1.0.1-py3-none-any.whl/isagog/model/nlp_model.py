"""
    A  model for Isagog NLP data objects
    (c) Isagog S.r.l. 2024, MIT License
"""
from typing import NamedTuple


class Word(NamedTuple):
    """
    NLP Data Model: Word
    """
    id: int
    text: str
    pos: str
    lemma: str
    span: dict


class NamedEntity(NamedTuple):
    """
    NLP Data Model: NamedEntity
    (not to be confused with KG Entity)
    """
    kind: str
    text: str
    span: dict