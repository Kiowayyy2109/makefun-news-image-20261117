#!/usr/bin/env python3
"""Entry point: publish the finished front page to /output/entry.png.

The artwork ships beside this file as artwork.png. This program copies it
byte-for-byte, then verifies the copy: identical SHA-256, PNG dimensions
exactly 1024x1024, and size at most 1 MiB. Standard library only, no
network, fully deterministic — repeated runs write identical bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "artwork.png")
OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.png")
MAX_BYTES = 1024 * 1024
EXPECTED_SIZE = (1024, 1024)
# Pinned digest of the shipped artwork. If artwork.png is ever swapped or
# corrupted, the program refuses to publish instead of emitting bad bytes.
EXPECTED_SHA256 = "fd989867ddcffe6c61adb584bb9ca8528dd2966b76823ceb454a5dc983c8caa0"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    with open(path, "rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    width, height = struct.unpack(">II", header[16:24])
    return (width, height)


def publish():
    """Validate the artwork, copy it atomically, and verify the result."""
    if not os.path.isfile(SOURCE) or os.path.islink(SOURCE):
        raise ValueError("artwork missing or symlinked: %s" % SOURCE)
    size = os.path.getsize(SOURCE)
    if size == 0 or size > MAX_BYTES:
        raise ValueError("artwork size out of bounds: %d bytes" % size)
    if png_dimensions(SOURCE) != EXPECTED_SIZE:
        raise ValueError("artwork must be exactly 1024x1024")
    source_digest = sha256_of(SOURCE)
    if source_digest != EXPECTED_SHA256:
        raise ValueError("artwork digest mismatch: %s" % source_digest)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tmp_path = OUTPUT_PATH + ".tmp"
    with open(SOURCE, "rb") as src, open(tmp_path, "wb") as dst:
        shutil.copyfileobj(src, dst, length=65536)
    os.replace(tmp_path, OUTPUT_PATH)
    if sha256_of(OUTPUT_PATH) != source_digest:
        raise ValueError("copy verification failed")
    if png_dimensions(OUTPUT_PATH) != EXPECTED_SIZE:
        raise ValueError("output dimensions wrong after copy")
    return size, source_digest


def main():
    try:
        size, digest = publish()
    except (OSError, ValueError) as exc:
        print("entry failed: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, 1024x1024, sha256 %s)" % (OUTPUT_PATH, size, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
