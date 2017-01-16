from __future__ import absolute_import, unicode_literals
from .celery import app
from . import PyPoetMod

@app.task
def poemAdd(url, si, sl, st, twoLines):
    output = "" # -1 random start index, 2 for 2 lines

    if twoLines:
        FAIL_LIMIT = 0

        for i in range(FAIL_LIMIT+1):
            output = PyPoetMod.getTwoLines("", url, si, 2, sl, st)
            if not "Could not complete" in output:
                break

        return output
    output = PyPoetMod.getOneLine("", url, si, 1, sl, st)
    return output