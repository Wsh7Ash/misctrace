"""
search.py — repository search primitives for a small review helper.

MVP: find a definition and references for a named symbol in a small set of
repositories by scanning source files for a plain-text occurrence plus a simple
identifier boundary check.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Location:
    repo: str
    file: str
    line: int
    kind: str
    snippet: str


@dataclass
class SymbolResult:
    symbol: str
    definitions: List[Location] = None
    references: List[Location] = None

    def __post_init__(self):
        if self.definitions is None:
            self.definitions = []
        if self.references is None:
            self.references = []


def _definition_patterns(symbol: str) -> re.Pattern:
    word = re.escape(symbol)
    return re.compile(
        rf"(?<!\w)(?:def |function |const {word}\s*=|let {word}\s*=|var {word}\s*=)\s*{word}\b"
    )


def find_definition(symbol: str, repo_root: Path) -> List[Location]:
    hits: List[Location] = []
    pattern = _definition_patterns(symbol)
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".h", ".cpp"}:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                hits.append(Location(repo=repo_root.name, file=str(path), line=i, kind="definition", snippet=line.strip()))
    return hits


def find_references(symbol: str, repo_root: Path, exclude_definitions: bool = True) -> List[Location]:
    hits: List[Location] = []
    word = re.escape(symbol)
    id_re = re.compile(rf"(?<!\w){word}\b")
    def_re = _definition_patterns(symbol) if exclude_definitions else None
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".h", ".cpp"}:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if not id_re.search(line):
                continue
            if def_re and def_re.search(line):
                continue
            hits.append(Location(repo=repo_root.name, file=str(path), line=i, kind="reference", snippet=line.strip()))
    return hits


def search_symbol(symbol: str, repos: List[Path]) -> SymbolResult:
    definitions: List[Location] = []
    references: List[Location] = []
    for root in repos:
        definitions.extend(find_definition(symbol, root))
        references.extend(find_references(symbol, root))
    return SymbolResult(symbol=symbol, definitions=definitions, references=references)
