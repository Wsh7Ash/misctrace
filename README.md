# misctrace

A small review helper that traces a named symbol across several repositories and records the call path it found. It is a review aid, not a full static analyzer: it records what it found and marks unresolved hops explicitly.

## What it does

- Search a set of repositories for a symbol definition and its references.
- Build a start-to-target trace from the found locations.
- Mark hops that could not be resolved.
- Emit a trace report with file paths, line numbers, and the status of each hop.

## Run locally

```bash
cd misctrace
python cli.py start_symbol target_symbol repo1 repo2
```

The MVP search works on a small set of repository roots and a common set of source extensions. It is best for a small review where you want a concrete trace record rather than an assertion.

## Output

The report shows the start and target symbols, whether the trace was resolved, and each hop with its locations or a missing marker.

## Limitations

- This is a simple text/identifier search. It does not understand full language semantics.
- Linkage in the MVP is a lightweight co-occurrence check, not a full data-flow or call-graph analysis.
- Large repositories may be slow; use it on a focused set of repos.

## Project structure

- `search.py` — repository search primitives.
- `trace.py` — trace builder.
- `report.py` — report formatting.
- `cli.py` — CLI entry point.
- `tests/` — pytest suite.
- `LICENSE` — MIT.
