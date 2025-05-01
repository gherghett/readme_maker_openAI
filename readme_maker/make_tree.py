import os
import pathlib
from pathspec import PathSpec

blacklist = ["bin", ".git", "node_modules", "venv", ".venv"]

import os
import pathlib
from pathspec import PathSpec

def load_gitignore(path: str) -> PathSpec:
    """
    Load .gitignore from the given directory path.
    """
    gitignore_path = pathlib.Path(path) / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path) as f:
            return PathSpec.from_lines("gitwildmatch", f.readlines())
    return PathSpec.from_lines("gitwildmatch", [])

def generate_tree(dir_path='.', indent='', spec = None, root_path=None):
    """Generate a visual tree structure as a string from a directory, respecting .gitignore."""
    if spec == None:
        spec=load_gitignore(dir_path)
    
    if root_path is None:
        root_path = os.path.abspath(dir_path)

    lines = []
    items = sorted(os.listdir(dir_path))
    for idx, item in enumerate(items):
        rel_path = os.path.relpath(os.path.join(dir_path, item), root_path)
        if spec and spec.match_file(rel_path):
            continue
        path = os.path.join(dir_path, item)
        is_last = idx == len(items) - 1
        connector = '└── ' if is_last else '├── '
        lines.append(indent + connector + item)
        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            lines.extend(generate_tree(path, indent + extension, spec, root_path))
    return lines


def tree_string(dir_path='.'):
    return "\n".join(generate_tree(dir_path))
