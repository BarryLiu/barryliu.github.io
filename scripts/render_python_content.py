#!/usr/bin/env python3
"""Convert public Python sources and saved notebooks into deterministic JSON."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

IGNORED_TAGS = {"hide-cell", "blog-ignore"}
SOURCE_ROOTS = ("app", "notebooks")


def markdown_to_html(source: str) -> str:
    """Render the small Markdown subset used by notebook narrative cells."""
    blocks: list[str] = []
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            value = " ".join(line.strip() for line in paragraph)
            blocks.append(f"<p>{html.escape(value)}</p>")
            paragraph.clear()

    for line in source.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush()
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{html.escape(heading.group(2))}</h{level}>")
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
    flush()
    return "\n".join(blocks)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_source(source: Path, relative: Path, output_root: Path) -> None:
    write_json(
        output_root / f"{relative.as_posix()}.json",
        {"id": relative.as_posix(), "kind": "source", "language": "python", "code": source.read_text(encoding="utf-8")},
    )


def render_output(output: dict, asset_root: Path, notebook_id: str, index: int) -> dict | None:
    output_type = output.get("output_type")
    if output_type == "stream":
        text = output.get("text", "")
        return {"type": "text", "text": "".join(text) if isinstance(text, list) else text}
    if output_type in {"execute_result", "display_data"}:
        data = output.get("data", {})
        if "text/plain" in data:
            value = data["text/plain"]
            return {"type": "text", "text": "".join(value) if isinstance(value, list) else value}
        for mime, suffix in (("image/png", ".png"), ("image/jpeg", ".jpg")):
            if mime in data:
                raw = data[mime]
                encoded = "".join(raw) if isinstance(raw, list) else raw
                digest = hashlib.sha256(encoded.encode()).hexdigest()[:12]
                filename = f"{index}-{digest}{suffix}"
                target = asset_root / notebook_id / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(base64.b64decode(encoded))
                return {"type": "image", "src": f"/python-content/{notebook_id}/{filename}", "mime": mime}
    if output_type == "error":
        return {"type": "error", "text": "\n".join(output.get("traceback", []))}
    return None


def render_notebook(source: Path, relative: Path, output_root: Path, asset_root: Path) -> None:
    notebook = json.loads(source.read_text(encoding="utf-8"))
    notebook_id = relative.with_suffix("").as_posix()
    cells: list[dict] = []
    for cell_index, cell in enumerate(notebook.get("cells", [])):
        tags = set(cell.get("metadata", {}).get("tags", []))
        if tags & IGNORED_TAGS:
            continue
        cell_source = cell.get("source", "")
        cell_source = "".join(cell_source) if isinstance(cell_source, list) else cell_source
        if cell.get("cell_type") == "markdown":
            cells.append({"type": "markdown", "source": cell_source, "html": markdown_to_html(cell_source)})
        elif cell.get("cell_type") == "code":
            outputs = [render_output(item, asset_root, notebook_id, cell_index) for item in cell.get("outputs", [])]
            cells.append({
                "type": "code",
                "source": cell_source,
                "executionCount": cell.get("execution_count"),
                "outputs": [item for item in outputs if item is not None],
            })
    write_json(
        output_root / f"{relative.as_posix()}.json",
        {"id": relative.as_posix(), "kind": "notebook", "language": notebook.get("metadata", {}).get("language_info", {}).get("name", "python"), "cells": cells},
    )


def generate(root: Path, destination: Path, assets: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    if assets.exists():
        shutil.rmtree(assets)
    for directory in SOURCE_ROOTS:
        source_root = root / directory
        if not source_root.exists():
            continue
        for source in sorted(source_root.rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(root)
            if "tests" in relative.parts or "__pycache__" in source.parts or ".ipynb_checkpoints" in source.parts:
                continue
            if source.suffix == ".py" and source.name != "__init__.py":
                render_source(source, relative, destination)
            elif source.suffix == ".ipynb":
                render_notebook(source, relative, destination, assets)


def snapshot(directory: Path) -> dict[str, bytes]:
    if not directory.exists():
        return {}
    return {path.relative_to(directory).as_posix(): path.read_bytes() for path in sorted(directory.rglob("*")) if path.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    destination = root / "src/generated/python-content"
    assets = root / "public/python-content"
    if args.check:
        before = (snapshot(destination), snapshot(assets))
        temporary = root / ".python-content-check"
        temp_assets = root / ".python-content-assets-check"
        generate(root, temporary, temp_assets)
        after = (snapshot(temporary), snapshot(temp_assets))
        shutil.rmtree(temporary, ignore_errors=True)
        shutil.rmtree(temp_assets, ignore_errors=True)
        if before != after:
            raise SystemExit("Python content is stale; run: uv run python scripts/render_python_content.py")
        return 0
    generate(root, destination, assets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
