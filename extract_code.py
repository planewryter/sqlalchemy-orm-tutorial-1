#!/usr/bin/env python

import os
import re
import subprocess

def extract_code(src_iterator):
    """extracts the code from a doctests source"""
    for line in src_iterator:
        line = line.replace("echo=False", "echo=True")
        if "doctest:" in line and "#" in line:
            comment_start = line.rfind("#", 0, line.rfind("doctest:"))
            if comment_start != -1:
                line = line[:comment_start].rstrip()
        if line.startswith(">>>") or line.startswith("..."):
            line = line[4:]
            if not line:
                yield " \n"
                have_break = False
            else:
                yield line.rstrip()+"\n"
                have_break = not line.strip()
        elif line.startswith("#"):
            yield line.rstrip()+"\n"
            have_break = False
        elif not line.strip() and not have_break:
            yield "\n"
            have_break = True

subprocess.call(["2to3", "-d", "-w", "-n", "--add-suffix=3", "-o", ".", "steps.txt"])

with open("steps3.txt", "w") as fix_file, open("steps.txt3", "r") as src_file:
    for line in src_file:
        fix_file.write(line)

os.remove("steps.txt3")

with open("blogapp2.py", "w") as py_file, open("steps.txt") as steps_file:
    py_file.write("#!/usr/bin/env python\n\n")
    have_break = True
    for line in extract_code(steps_file):
        py_file.write(line)

with open("blogapp3.py", "w") as py_file, open("steps3.txt") as steps_file:
    py_file.write("#!/usr/bin/env python\n\n")
    have_break = True
    for line in extract_code(steps_file):
        py_file.write(line)
