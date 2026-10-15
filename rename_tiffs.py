#!/usr/bin/env python3
"""
Batch-renames .tif/.tiff files in a folder by appending "_N" before the
extension, where N is a sequential number.

Example:
    image.tif      -> image_1.tif
    scan.tiff       -> scan_2.tiff

Usage:
    python rename_tiffs.py /path/to/folder
    python rename_tiffs.py /path/to/folder --start 1
"""

import argparse
import os
from pathlib import Path


def rename_tiffs(folder: Path, start: int = 1) -> None:
    tiff_files = sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in (".tif", ".tiff")
    )

    if not tiff_files:
        print(f"No .tif/.tiff files found in {folder}")
        return

    count = start
    for f in tiff_files:
        new_name = f"{count}_{f.stem}{f.suffix}"
        new_path = f.with_name(new_name)
        f.rename(new_path)
        print(f"{f.name} -> {new_name}")
        count += 1

    print(f"\nRenamed {len(tiff_files)} file(s).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append _N to TIFF filenames.")
    parser.add_argument("folder", type=str, help="Path to the folder containing TIFF files")
    parser.add_argument("--start", type=int, default=1, help="Starting number (default: 1)")
    args = parser.parse_args()

    folder_path = Path(args.folder)
    if not folder_path.is_dir():
        raise SystemExit(f"Error: '{folder_path}' is not a valid folder.")

    rename_tiffs(folder_path, args.start)
