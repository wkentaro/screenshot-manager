#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import os
import os.path as osp
import pkg_resources
import re
import shutil
import sys


def get_locations(uname):
    locations = []
    if uname == "Linux":
        locations = [osp.expanduser("~/Pictures"), osp.expanduser("~/Videos")]
        config_file = osp.expanduser("~/.config/user-dirs.dirs")
        if osp.exists(config_file):
            locations = []
            with open(config_file) as f:
                for line in f:
                    for pattern in [
                        r'^XDG_PICTURES_DIR="(.*)"$',
                        r'^XDG_VIDEOS_DIR="(.*)"$',
                    ]:
                        m = re.match(pattern, line)
                        if not m:
                            continue
                        location = osp.expanduser(m.groups()[0])
                        location = location.replace(
                            "$HOME", osp.expanduser("~")
                        )
                        if location not in locations:
                            locations.append(location)
    elif uname == "Darwin":
        locations = [os.path.expanduser("~/Desktop")]
    return locations


default_config = {
    "Darwin": {
        "from_location": get_locations("Darwin"),
        "from_format": [
            "Screen Shot %Y-%m-%d at %H.%M.%S",
            "Kapture %Y-%m-%d at %H.%M.%S",
        ],
        "to_format": "%Y-%m-%d_%H-%M-%S",
    },
    "Linux": {
        "from_location": get_locations("Linux"),
        "from_format": [
            "Screenshot from %Y-%m-%d %H-%M-%S",
            "Screencast %Y-%m-%d %H:%M:%S",
        ],
        "to_format": "%Y-%m-%d_%H-%M-%S",
    },
}


def copyfile_safe(from_filename, to_filename, verbose=False):
    to_filename_base, to_filename_ext = osp.splitext(to_filename)

    count = 1
    while True:
        if not osp.exists(to_filename):
            break
        to_filename = "{base} ({count}){ext}".format(
            base=to_filename_base, count=count, ext=to_filename_ext
        )
        count += 1

    if verbose:
        print("Coping file:", from_filename, "->", to_filename)
    shutil.copy2(from_filename, to_filename)


def main():
    sysname = os.uname()[0]
    config = default_config.get(sysname, {})

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Show version of this software",
    )
    parser.add_argument(
        "--from-location",
        help="Location from which screenshots are copied",
        default=config.get("from_location"),
    )
    parser.add_argument(
        "--to-location",
        help="Location to which screenshots are copied.",
    )
    parser.add_argument(
        "--from-format",
        help="Expected format of screenshots name",
        default=config.get("from_format"),
        nargs="+",
    )
    parser.add_argument(
        "--to-format",
        help="Format of screenshots name to which they are renamed",
        default=config.get("to_format"),
    )
    parser.add_argument(
        "--copy-same",
        help="Copy even if the file has the same name. NOTE: this may "
        "cause many copies if you changed the file already uploaded.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose mode",
        action="store_true",
    )
    args = parser.parse_args()

    if args.version:
        version = pkg_resources.get_distribution("screenshot-manager").version
        print("screenshot-manager", version)
        sys.exit()

    if args.to_location is None:
        parser.print_usage(file=sys.stderr)
        print(
            "screenshot_manager: error: "
            "the following arguments are required: --to-location",
            file=sys.stderr,
        )
        sys.exit(2)

    if args.verbose:
        print("Configurations:")
        for key, value in sorted(args.__dict__.items()):
            print("  {}: {}".format(key, value))
        print()

    for from_location in args.from_location:
        if not osp.exists(from_location):
            print("Directory does not exist:", from_location, file=sys.stderr)
            continue
        for basename in sorted(os.listdir(from_location)):
            from_filename = osp.join(from_location, basename)

            basename_base, basename_ext = osp.splitext(basename)

            matched = []
            for pattern in args.from_format:
                try:
                    dt = datetime.datetime.strptime(basename_base, pattern)
                    matched.append(True)
                except ValueError:
                    matched.append(False)
                    continue
                to_filename = osp.join(
                    args.to_location,
                    dt.strftime(args.to_format) + basename_ext,
                )

                if osp.exists(to_filename):
                    if not args.copy_same:
                        print(
                            "Skipping file that has the same name:",
                            from_filename,
                        )
                        continue

                    from_stat = os.stat(from_filename)
                    to_stat = os.stat(to_filename)
                    if int(from_stat.st_mtime) == int(to_stat.st_mtime):
                        if args.verbose:
                            print("Skipping unchanged file:", from_filename)
                        continue

                copyfile_safe(from_filename, to_filename, verbose=args.verbose)

            if not any(matched) and args.verbose:
                print("Skipping unmatched file:", from_filename)
