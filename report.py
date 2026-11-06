"""
report.py — trace report formatting.
"""

from __future__ import annotations

from typing import List

from trace import Hop, Trace


def format_trace(trace: Trace) -> str:
    lines: List[str] = []
    lines.append("Trace report")
    lines.append("============")
    lines.append(f"start: {trace.start}")
    lines.append(f"target: {trace.target}")
    lines.append(f"resolved: {trace.resolved}")
    if trace.note:
        lines.append(f"note: {trace.note}")
    lines.append("")
    for hop in trace.hops:
        lines.append(f"- {hop.symbol} [{hop.status}]")
        if hop.locations:
            for loc in hop.locations:
                lines.append(f"    {loc.repo}:{loc.file}:{loc.line} ({loc.kind})")
                lines.append(f"      {loc.snippet}")
        else:
            lines.append("    (no locations)")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
