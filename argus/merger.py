"""Merge strategies for combining generated files with existing user content."""

import json
import re
from typing import Any, Protocol

from argus import ArgusError


class FileMerger(Protocol):
    """Combine generated content with existing file content."""

    def merge(self, existing: str, generated: str) -> str | None:
        """Return merged content, or None to leave the existing file untouched."""
        ...


class JsonMerger:
    """Deep-merge generated JSON over existing JSON, preserving unknown keys."""

    _UNION_KEYS = frozenset({"instructions"})

    def merge(self, existing: str, generated: str) -> str | None:
        """Return merged JSON text, or None if the existing text is not parseable JSON."""
        generated_data = self._parse_generated(generated)
        try:
            existing_data: Any = json.loads(existing)
        except json.JSONDecodeError:
            return None
        if not isinstance(existing_data, dict):
            return None
        return json.dumps(self._merge_dicts(existing_data, generated_data), indent=2)

    def _parse_generated(self, generated: str) -> dict[str, Any]:
        try:
            data: Any = json.loads(generated)
        except json.JSONDecodeError as e:
            raise ArgusError(f"Generated content is not valid JSON: {e}") from e
        if not isinstance(data, dict):
            raise ArgusError("Generated content for JSON merge must be an object.")
        return data

    def _merge_dicts(
        self, existing: dict[str, Any], generated: dict[str, Any]
    ) -> dict[str, Any]:
        merged = dict(existing)
        for key, value in generated.items():
            if key not in merged:
                merged[key] = value
            elif key in self._UNION_KEYS:
                merged[key] = self._union(merged[key], value)
            elif isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_dicts(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _union(self, existing: Any, generated: Any) -> list[Any]:
        existing_items = existing if isinstance(existing, list) else [existing]
        generated_items = generated if isinstance(generated, list) else [generated]
        return existing_items + [g for g in generated_items if g not in existing_items]


class MarkedBlockMerger:
    """Carry foreign HTML-comment-marked blocks across regeneration."""

    _BLOCK_RE = re.compile(
        r"<!--\s*(?P<name>[\w-]+:[\w-]+):start\s*-->.*?<!--\s*(?P=name):end\s*-->",
        re.DOTALL,
    )

    def merge(self, existing: str, generated: str) -> str | None:
        """Append preserved marked blocks to generated content, or return generated unchanged."""
        blocks = [m.group(0) for m in self._BLOCK_RE.finditer(existing)]
        if not blocks:
            return generated
        return generated.rstrip("\n") + "\n\n" + "\n\n".join(blocks)
