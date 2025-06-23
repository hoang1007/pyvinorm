import importlib.resources as pkg_resources
import os
from pathlib import Path
import locale

locale.setlocale(locale.LC_ALL, "vi_VN.utf8")

if __name__ == "__main__":
    for resource in pkg_resources.contents("pyvinorm.resources.mapping"):
        if resource.endswith(".txt"):
            with pkg_resources.path("pyvinorm.resources.mapping", resource) as path:
                with open(path, "r", encoding="utf-8") as f:
                    lines = []
                    for line in f:
                        lines.append(line.strip())
                # Sort lines using locale-aware sorting
                # Sort by key first and then by value
                lines.sort(key=lambda x: tuple(locale.strxfrm(t) for t in x.split("#")))

                with open(path, "w", encoding="utf-8") as f:
                    for line in lines:
                        f.write(line + "\n")
            print(f"Sorted {resource} successfully.")
