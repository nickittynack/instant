import bdb
import cmd
import copy
import inspect
import os
import pdb
import sys
import tempfile
import time
import traceback
from collections import defaultdict
from pathlib import Path

import requests_cache

requests_cache.install_cache("demo_cache")


class Tracer(pdb.Pdb):

    _run = 0

    def __init__(self, *args, **kwargs):
        self._history = []
        self._hcount = 0
        self._previous = None

        self._init = False

        self._line = None

        self._previous_line = None

        super(Tracer, self).__init__(*args, **kwargs)

    def user_call(self, frame, args):
        name = frame.f_code.co_name or "<unknown>"
        self.set_continue()

    def insert_changes(self, c, line):
        changed_line = line != self._line

        old_line = self._line

        self._line = line

        try:
            current_keys = self._history[self._hcount]

            already_visited = changed_line and line in current_keys

            gone_backwards = old_line is not None and line < old_line

            if already_visited or gone_backwards:
                self._hcount += 1
                raise IndexError

            current_iteration = self._history[self._hcount]
        except IndexError:
            self._history.append({})
            current_iteration = self._history[self._hcount]

        if line in current_iteration:
            current_line = current_iteration[line]
        else:
            current_line = {}
            current_iteration[line] = current_line

        for k, v in c.items():
            if inspect.ismodule(v) or inspect.isfunction(v) or inspect.isgenerator(v):
                v = str(v)
            if isinstance(v, list) or isinstance(v, dict):
                v = copy.deepcopy(v)
            current_line[k] = v

    def trace_dispatch(self, frame, event, arg):
        if self.break_here(frame):

            if event == "line":
                line = self._previous_line or frame.f_lineno
            else:
                line = frame.f_lineno

            self.update_changes(frame, line)
            self._previous_line = frame.f_lineno

        return pdb.Pdb.trace_dispatch(self, frame, event, arg)

    def update_changes(self, frame, line_number=None):
        name = frame.f_code.co_name or "<unknown>"

        filename = self.canonic(frame.f_code.co_filename)

        def should_track(k, v):
            if k.startswith("_"):
                return False

            if k.startswith("."):
                return False
            if inspect.isfunction(v):
                return False

            if inspect.isclass(v):
                return False

            return True

        def filtered(d):
            return {k: v for k, v in d.items() if should_track(k, v)}

        d = filtered(frame.f_globals)
        d.update(filtered(frame.f_locals))

        p = self._previous

        def include_in_history(k, v, p):
            if p is None:
                return True

            if k not in p:
                return True

            if p[k] != v:
                return True

        changes = {k: v for k, v in d.items() if include_in_history(k, v, p)}

        line_number = line_number or frame.f_lineno

        self.insert_changes(changes, line_number)

        self._previous = copy.deepcopy(d)

    def user_line(self, frame):
        self.set_continue()

    def user_return(self, frame, value):
        self.set_continue()  # continue

    def user_exception(self, frame, exception):
        self.set_continue()  # continue

    def trace_code_file(self, path, linecount=None):
        path = str(path)

        linecount = linecount or len(Path(path).read_text().splitlines())

        for x in range(1, linecount + 1):
            self.set_break(path, x)

        def parse_message(s):
            if "module named" in s:
                return
            b, f = s.split(" line ")
            num = f.rstrip(")")

            return int(num), b.split("(")[0].strip()

        try:
            self._runscript(str(path))
        except Exception as e:
            t = e.__traceback__

            extracted = traceback.extract_tb(t)
            line = extracted[-1].lineno
            k = type(e).__name__

            if k in ("SyntaxError", "ImportError", "IndentationError"):
                line, msg = parse_message(str(e))
            else:
                msg = str(e)
            self.insert_changes({k: msg}, line)
            return

        return self._history

    def trace_code(self, code):
        with tempfile.TemporaryDirectory() as tmpdirname:
            path = Path(tmpdirname) / "script.py"
            path.write_text(code)
            return self.trace_code_file(path, linecount=None)

    @property
    def history(self):
        return self._history


def trace_code(code):
    t = Tracer()
    t.trace_code(code)
    return t.history


def trace_code_file(f):
    t = Tracer()
    t.trace_code_file(f)
    return t.history
