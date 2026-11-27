"""Hand the drawn wire sheet to the grader.

The kit's starter copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`) in
Node; this is the same move in the Python the rules allow. The image is already
drawn by render8.py at build time, so the entry run only copies bytes: the judge
sees exactly the file committed here. Each path is tried in turn so a read-only
parent cannot end the run.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE / "entry.png"


def copy_into(folder):
    target = Path(folder) / "entry.png"
    Path(folder).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PAGE, target)
    return target


def main():
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    for folder in (wanted, "/tmp", str(Path.cwd()), str(HERE)):
        try:
            target = copy_into(folder)
        except OSError as exc:
            print("cannot write", folder, exc)
            continue
        print("wrote", target, target.stat().st_size, "bytes")
        return 0
    sys.exit("no writable output directory")


if __name__ == "__main__":
    main()
