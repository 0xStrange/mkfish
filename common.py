#!/usr/bin/env python3

import contextlib
import io
import os
import sys


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def print_between_eols(s):
    assert(len(s) >= 2)
    assert(s[0] == '\n')
    assert(s[-1] == '\n')
    print(s[1:-1])


def update_file(file_path, new_content):
    old_content = ''
    if os.path.isfile(file_path):
        with open(file_path, mode='r') as fh:
            old_content = fh.read()

    if old_content == new_content:
        print('[ up-to-date ] %s' % file_path)
        return

    with open(file_path, mode='w') as fh:
        fh.write(new_content)

    print('[ updated ] %s' % file_path)
    pass


def capture_output(function, *args, **kwargs):
    with io.StringIO() as f, contextlib.redirect_stdout(f):
        function(*args, **kwargs)
        s = f.getvalue()
    return s


def generate_file(file_path, generator, *args, **kwargs):
    s = capture_output(generator, *args, **kwargs)
    update_file(file_path, s)
