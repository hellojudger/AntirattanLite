import os

for i in os.listdir("."):
    if i not in ["1.cpp", "2.cpp", "clean.py", "run.py", "Makefile", "1.in", ".vscode", "core", "README.md"]:
        os.remove(i)

