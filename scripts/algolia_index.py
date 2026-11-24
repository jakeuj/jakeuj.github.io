#!/usr/bin/env python3
"""Prepare the Writerside search index for the Algolia publisher (standard library only).

For every JSON record in the index directory:
* drop contentBoost, which the publisher rejects,
* trim content so the record stays under Algolia's 10,000-byte limit. The publisher adds a few dozen
  bytes of its own, so LIMIT leaves room for them.

A record over the limit makes the publisher throw; its JVM then never exits, so the job hangs.
"""

import argparse
import json
import sys
from pathlib import Path

LIMIT = 9700


def size(record):
    return len(json.dumps(record, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def trim(record, limit=LIMIT):
    """Shorten content until the record fits. Returns True when it was trimmed."""
    over = size(record) - limit
    if over <= 0:
        return False
    content = record.get("content")
    if not isinstance(content, str) or not content:
        raise ValueError(f"record is {size(record)} bytes and has no content to trim: {record.get('objectID')}")
    low, high = 0, len(content)  # longest prefix (in characters) that still fits
    while low < high:
        middle = (low + high + 1) // 2
        record["content"] = content[:middle].rstrip() + "…"
        if size(record) <= limit:
            low = middle
        else:
            high = middle - 1
    if low == 0:
        raise ValueError(f"record does not fit: {record.get('objectID')}")
    record["content"] = content[:low].rstrip() + "…"
    return True


def normalize(directory, limit=LIMIT):
    trimmed = []
    for path in sorted(Path(directory).rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        records = data if isinstance(data, list) else [data]
        for record in records:
            if not isinstance(record, dict):
                continue
            record.pop("contentBoost", None)
            if "objectID" in record and trim(record, limit):
                trimmed.append((record["objectID"], size(record)))
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    for object_id, bytes_ in trimmed:
        print(f"::warning::Trimmed search record {object_id} to {bytes_} bytes")
    print(f"Normalized {len(list(Path(directory).rglob('*.json')))} index files, trimmed {len(trimmed)} records")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("directory", type=Path)
    normalize(parser.parse_args().directory)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"::error::{error}")
        sys.exit(1)
