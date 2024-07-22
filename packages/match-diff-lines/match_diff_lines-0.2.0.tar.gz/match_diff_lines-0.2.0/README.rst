match-diff-lines
================

Match a diff to a list of lines from linters and other tools like flake8 or ruff.


Installation
------------

Best to install into a virtual environment with a Python installer like ``pip`` or similar.


Usage
-----

Invoke ``python -m match_diff_lines diff_file tool_output``.
The ``diff_file`` is a file containing the unified diff output you want to check against.
The ``tool_output`` contains the output of your linter/tool which contains lines in the form of ``filename:line_num`` for example::

    match_diff_lines.py:59:39: E271 multiple spaces after keyword

If any lines are contained in the diff, then they are printed and exit code 1 is returned.

With bash or zsh you can use temporary named pipes like this::

    % python -m match_diff_lines <(git diff HEAD^) <(ruff check)
