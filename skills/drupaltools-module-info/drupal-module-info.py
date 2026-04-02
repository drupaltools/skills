#!/usr/bin/env python3
"""
drupal-module-info: Find the Drupal module or theme owning a given file.
Usage: drupal-module-info.py <file_or_directory_path>
No external dependencies required.
"""

import sys
import os
import glob
import re


def find_info_yml(start_path):
    path = os.path.abspath(start_path)
    if os.path.isfile(path):
        path = os.path.dirname(path)
    while True:
        matches = glob.glob(os.path.join(path, "*.info.yml"))
        if matches:
            return matches[0]
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def parse_info_yml(info_file):
    with open(info_file, "r") as f:
        content = f.read()

    def scalar(key):
        m = re.search(rf"^{key}:\s*(.+)$", content, re.MULTILINE)
        return m.group(1).strip().strip('"').strip("'") if m else "not set"

    def list_values(key):
        # Collect indented list items under the key
        m = re.search(rf"^{key}:\s*\n((?:[ \t]+-[^\n]*\n?)*)", content, re.MULTILINE)
        if not m:
            return []
        return re.findall(r"-\s*(.+)", m.group(1))

    machine_name = os.path.basename(info_file).replace(".info.yml", "")
    version = scalar("version")
    if version == "VERSION":
        version = "VERSION (dev checkout)"

    return {
        "machine_name": machine_name,
        "type":         scalar("type"),
        "description":  scalar("description"),
        "version":      version,
        "core":         scalar("core_version_requirement"),
        "dependencies": list_values("dependencies"),
        "info_file":    info_file,
    }


def report(info):
    m = info["machine_name"]
    deps = ", ".join(info["dependencies"]) if info["dependencies"] else "none"
    print(f"Machine name : {m}")
    print(f"Type         : {info['type']}")
    print(f"Description  : {info['description']}")
    print(f"Version      : {info['version']}")
    print(f"Core req     : {info['core']}")
    print(f"Dependencies : {deps}")
    print(f"Drupal.org   : http://dgo.to/{m}")
    print(f"Info file    : {info['info_file']}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file_or_directory_path>")
        sys.exit(1)

    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"ERROR: Path not found: {target}")
        sys.exit(1)

    info_file = find_info_yml(target)
    if not info_file:
        print(f"ERROR: No *.info.yml found in any parent directory of: {target}")
        sys.exit(1)

    report(parse_info_yml(info_file))


if __name__ == "__main__":
    main()
