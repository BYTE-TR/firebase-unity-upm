"""Mirror Firebase Unity SDK UPM tarballs into git-installable package folders.

Usage: python sync.py <version> [module ...]
Example: python sync.py 14.1.0 app analytics remote-config
"""
import io
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

REGISTRY = "https://dl.google.com/games/registry/unity"
DEFAULT_MODULES = ["app", "analytics", "remote-config"]
# GitHub rejects files of 100 MiB or more without LFS.
GITHUB_FILE_LIMIT = 100 * 1024 * 1024

ROOT = Path(__file__).resolve().parent


def sync(version, module):
    name = f"com.google.firebase.{module}"
    url = f"{REGISTRY}/{name}/{name}-{version}.tgz"
    print(f"Downloading {url}")
    with urllib.request.urlopen(url) as response:
        data = response.read()

    target = ROOT / name
    if target.exists():
        shutil.rmtree(target)
    target.mkdir()

    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.name.startswith("package/") or not (member.isfile() or member.isdir()):
                continue
            member.name = member.name[len("package/"):]
            if member.size >= GITHUB_FILE_LIMIT:
                sys.exit(f"{name}/{member.name} is {member.size} bytes; GitHub needs LFS for it")
            archive.extract(member, target, filter="data")
    print(f"  -> {target.name}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    version = sys.argv[1]
    modules = sys.argv[2:] or DEFAULT_MODULES
    if "app" not in modules:
        modules.insert(0, "app")
    for module in modules:
        sync(version, module)


if __name__ == "__main__":
    main()
