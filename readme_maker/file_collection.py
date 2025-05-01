import os
import pathlib
from typing import List, Set
from pathspec import PathSpec

MAXS_CHARS = 17_000
# Default blacklist — can be overridden
DEFAULT_BLACKLIST = {"node_modules", "__pycache__", ".git", ".venv", "venv"}

def load_gitignore(path: str) -> PathSpec:
    """
    Load .gitignore from the given directory path.
    """
    gitignore_path = pathlib.Path(path) / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path) as f:
            return PathSpec.from_lines("gitwildmatch", f.readlines())
    return PathSpec.from_lines("gitwildmatch", [])

def collect_files(
    target_path: str,
    blacklist: Set[str] = None
) -> List[str]:
    if blacklist is None:
        blacklist = DEFAULT_BLACKLIST

    gitignore_spec = load_gitignore(target_path)
    collected_files = []

    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in blacklist]
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), target_path)
            full_path = os.path.join(target_path, rel_path)
            if (
                file in blacklist or
                any(part in pathlib.Path(rel_path).parts for part in blacklist) or
                gitignore_spec.match_file(rel_path)
            ):
                continue
            collected_files.append(full_path)

    return collected_files


def get_combined_file_content(directory, max_chars=MAXS_CHARS):
    files = collect_files(directory)
    total_chars = 0
    combined_text = ""

    for file in files:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if total_chars + len(content) > max_chars:
                    print(f"Skipping {file} — would exceed {max_chars} characters.")
                    continue
                combined_text += f"\n\n# FILE: {file}\n{content}"
                total_chars += len(content)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    print(f"Included {len(files)} files with {total_chars} total characters.")
    return combined_text if total_chars > 0 else None

def get_combined_file_content_from_list(file_paths, max_chars=10_000):
    """
    Takes a list of file paths, reads their content, and returns a single combined string.
    Skips files if the combined content exceeds max_chars.
    """
    combined_text = ""
    total_chars = 0
    included_files = 0

    for file in file_paths:
        file = file.strip()  # In case the model added extra whitespace
        file = strip_quotes(file)
        if not file or not os.path.exists(file):
            print(f"Skipping missing or empty path: '{file}'")
            continue

        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if total_chars + len(content) > max_chars:
                    print(f"Skipping {file} — would exceed {max_chars} characters.")
                    continue
                combined_text += f"\n\n# FILE: {file}\n{content}"
                total_chars += len(content)
                included_files += 1
        except Exception as e:
            print(f"Error reading {file}: {e}")

    print(f"Included {included_files} files with {total_chars} total characters.")
    return combined_text if total_chars > 0 else None


def strip_quotes(s):
    quote_chars = '"\'“”‘’«»‹›`´'
    return s.strip(quote_chars)
