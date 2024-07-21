from __future__ import annotations

from pathlib import Path
import collections
import re
import sys


__version__ = "0.1.0"


DIFF_HUNK_REGEXP = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@.*$")
FILE_POS_REGEXP = re.compile(r"^\s*(.+?):(\d+)(:\d+)?.*$")


# originally from flake8
def parse_unified_diff(fd) -> dict[str, set[int]]:
    number_of_rows = None
    current_path = None
    parsed_paths: dict[str, set[int]] = collections.defaultdict(set)
    for line in fd:
        if number_of_rows:
            if not line or line[0] != "-":
                number_of_rows -= 1
            # We're in the part of the diff that has lines starting with +, -,
            # and ' ' to show context and the changes made. We skip these
            # because the information we care about is the filename and the
            # range within it.
            # When number_of_rows reaches 0, we will once again start
            # searching for filenames and ranges.
            continue

        # NOTE(sigmavirus24): Diffs that we support look roughly like:
        #    diff a/file.py b/file.py
        #    ...
        #    --- a/file.py
        #    +++ b/file.py
        # Below we're looking for that last line. Every diff tool that
        # gives us this output may have additional information after
        # ``b/file.py`` which it will separate with a \t, e.g.,
        #    +++ b/file.py\t100644
        # Which is an example that has the new file permissions/mode.
        # In this case we only care about the file name.
        if line[:3] == "+++":
            current_path = line[4:].split("\t", 1)[0]
            # NOTE(sigmavirus24): This check is for diff output from git.
            if current_path[:2] == "b/":
                current_path = current_path[2:].rstrip()
            # We don't need to do anything else. We have set up our local
            # ``current_path`` variable. We can skip the rest of this loop.
            # The next line we will see will give us the hung information
            # which is in the next section of logic.
            continue

        if (hunk_match := DIFF_HUNK_REGEXP.match(line)):
            (row, number_of_rows) = (
                1 if not group else int(group) for group in hunk_match.groups()
            )
            parsed_paths[current_path].update(range(row, row + number_of_rows))

    # We have now parsed our diff into a dictionary that looks like:
    #    {'file.py': set(range(10, 16), range(18, 20)), ...}
    return parsed_paths


def match_lines(fd, diff):
    for line in fd:
        if not (m := FILE_POS_REGEXP.match(line)):
            continue
        if not (lines := diff.get(m[1])):
            continue
        if int(m[2]) in lines:
            yield line


if __name__ == "__main__":
    with Path(sys.argv[1]).open() as f:
        diff = parse_unified_diff(f)
    had_errors = False
    with Path(sys.argv[2]).open() as f:
        for line in match_lines(f, diff):
            had_errors = True
            print(line)  # noqa: T201 - this is a cli tool
    if had_errors:
        sys.exit(1)
