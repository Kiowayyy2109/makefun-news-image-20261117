#!/usr/bin/env python3
"""news-image-20261117 entry: copy the bundled front-page artwork to
/output/entry.png, byte-for-byte, and verify it.

Deterministic: the same input bytes always produce the same output bytes.
Standard library only; no network access.
"""

import hashlib
import struct
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "artwork.png"
DEST = Path("/output/entry.png")
MAX_BYTES = 1_048_576
EXPECTED_SHA256 = "ceded56bf4ce114559c752b4be2d4af10e661ad3efb8e727ce46f062786fdd0c"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(data):
    """Read width/height from the PNG IHDR chunk (stdlib only)."""
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("missing PNG IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    if not SOURCE.is_file():
        print(f"missing artwork: {SOURCE}", file=sys.stderr)
        return 1
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        print(f"artwork too large: {len(data)} bytes", file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("artwork hash mismatch: bundled artwork was modified",
              file=sys.stderr)
        return 1
    try:
        width, height = png_dimensions(data)
    except ValueError as exc:
        print(f"invalid artwork: {exc}", file=sys.stderr)
        return 1
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"artwork is {width}x{height}, expected "
              f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}", file=sys.stderr)
        return 1
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(data)
    written = sha256_of(DEST)
    if written != EXPECTED_SHA256:
        print("self-check failed: output hash mismatch", file=sys.stderr)
        return 1
    print(f"wrote {DEST} ({len(data)} bytes, "
          f"{width}x{height}, sha256 {written})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
