"""
trace.py — trace builder for a start-to-target symbol path.

MVP: given a start symbol and a target symbol, build a trace from the
definitions and references found across the provided repos. Unresolved hops are
marked explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from search import Location, SymbolResult, search_symbol


@dataclass
class Hop:
    symbol: str
    locations: List[Location] = field(default_factory=list)
    status: str = "found"  # found | missing


@dataclass
class Trace:
    start: str
    target: str
    hops: List[Hop] = field(default_factory=list)
    resolved: bool = False
    note: str = ""


def build_trace(start: str, target: str, repos: List[Path]) -> Trace:
    start_result = search_symbol(start, repos)
    target_result = search_symbol(target, repos)

    hops: List[Hop] = []
    hops.append(Hop(symbol=start, locations=list(start_result.definitions), status="found" if start_result.definitions else "missing"))
    hops.append(Hop(symbol=target, locations=list(target_result.definitions), status="found" if target_result.definitions else "missing"))

    if start_result.definitions and target_result.definitions:
        linked = False
        for r in repos:
            try:
                if not r.exists():
                    continue
                if r.is_file():
                    text = r.read_text(encoding="utf-8", errors="replace")
                else:
                    text = ""
                    for p in r.rglob("*"):
                        if p.is_file():
                            try:
                                text += p.read_text(encoding="utf-8", errors="replace")
                            except OSError:
                                continue
            except OSError:
                continue
            if start in text and target in text:
                linked = True
                break
        if linked:
            hops.append(Hop(symbol=f"{start}->{target}", locations=list(target_result.references), status="found"))
            return Trace(start=start, target=target, hops=hops, resolved=True)

    hops.append(Hop(symbol=f"{start}->{target}", status="missing"))
    return Trace(start=start, target=target, hops=hops, resolved=False, note="No direct linkage found in MVP search scope")
