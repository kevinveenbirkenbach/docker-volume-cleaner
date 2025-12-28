#!/usr/bin/env python3

import argparse
import subprocess
import re
import sys
from pathlib import Path
import shutil

VOLUME_BASE_PATH = Path("/var/lib/docker/volumes")

def get_anonymous_volumes():
    result = subprocess.run(
        ["docker", "volume", "ls", "--format", "{{.Name}}"],
        stdout=subprocess.PIPE,
        text=True
    )
    return [
        vol for vol in result.stdout.splitlines()
        if re.fullmatch(r"[a-f0-9]{64}", vol)
    ]

def get_mount_path(volume):
    containers = subprocess.run(["docker", "ps", "-q"], stdout=subprocess.PIPE, text=True).stdout.split()
    for container_id in containers:
        mount_path = subprocess.run(
            [
                "docker", "inspect", container_id,
                "--format", f"{{{{range .Mounts}}}}{{{{if eq .Name \"{volume}\"}}}}{{{{.Destination}}}}{{{{end}}}}{{{{end}}}}"
            ],
            stdout=subprocess.PIPE,
            text=True
        ).stdout.strip()
        if mount_path:
            return mount_path
    return None

def is_volume_used(volume):
    result = subprocess.run(
        ["docker", "ps", "-aq", "--filter", f"volume={volume}"],
        stdout=subprocess.PIPE,
        text=True
    )
    return bool(result.stdout.strip())

def cleanup_symlink(volume):
    volume_dir = VOLUME_BASE_PATH / volume
    data_path = volume_dir / "_data"

    if data_path.is_symlink():
        target_path = data_path.resolve()
        print(f"_data of volume {volume} is a symlink to {target_path}.")
        try:
            print(f"Removing symlink: {data_path}")
            data_path.unlink()
            if target_path.exists():
                print(f"Removing symlink target directory: {target_path}")
                shutil.rmtree(target_path)
        except Exception as e:
            print(f"Failed to clean up _data symlink or its target for {volume}: {e}")

def delete_volume(volume):
    cleanup_symlink(volume)
    subprocess.run(["docker", "volume", "rm", volume])

def main():
    parser = argparse.ArgumentParser(description="Remove unused anonymous Docker volumes.")
    parser.add_argument("whitelist", nargs="?", default="", help="Space-separated list of whitelisted volume IDs")
    parser.add_argument("--no-confirmation", action="store_true", help="Skip confirmation before deleting volumes")
    args = parser.parse_args()

    whitelist = set(args.whitelist.split())

    anonymous_volumes = get_anonymous_volumes()
    if not anonymous_volumes:
        print("No anonymous volumes found.")
        sys.exit(0)

    to_delete = []

    print("Checking anonymous volumes...\n")

    for volume in anonymous_volumes:
        if volume in whitelist:
            print(f"Volume {volume} is whitelisted and will be skipped.")
            continue

        mount_path = get_mount_path(volume)
        if mount_path == "/var/www/bootstrap":
            print(f"Volume {volume} is mounted at /var/www/bootstrap and will be skipped.")
            continue

        if not is_volume_used(volume):
            print(f"Volume {volume} is not used by any running containers.")
            to_delete.append(volume)
        else:
            print(f"Volume {volume} is still used and will not be deleted.")

    if not to_delete:
        print("\nNo unused anonymous volumes to delete.")
        sys.exit(0)

    print("\nThe following volumes will be deleted:")
    for vol in to_delete:
        print(f"  - {vol}")

    if not args.no_confirmation:
        confirm = input("\nDo you want to proceed? [y/N]: ").lower()
        if confirm != "y":
            print("Aborted.")
            sys.exit(1)

    for volume in to_delete:
        delete_volume(volume)

    print("\nUnused anonymous volumes deleted.")

if __name__ == "__main__":
    main()
