"""
tests/test_report.py — report formatting tests.
"""
from __future__ import annotations

from trace import Hop, Trace
from report import format_trace


def test_report_shows_symbols():
    trace = Trace(start="start", target="target", hops=[Hop(symbol="start", locations=[], status="found")], resolved=True)
    report = format_trace(trace)
    assert "start: start" in report
    assert "target: target" in report
    assert "resolved: True" in report


def test_report_shows_missing_hop():
    trace = Trace(start="start", target="target", hops=[Hop(symbol="start->target", status="missing")], resolved=False, note="no linkage")
    report = format_trace(trace)
    assert "resolved: False" in report
    assert "no linkage" in report
