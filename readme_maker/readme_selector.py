from typing import Callable, List

MAXS_CHARS = 17_000

def get_tree_with_file_sizes(
    directory: str,
    collect_files_fn: Callable[[str], List[str]],
    tree_string_fn: Callable[[str], str],
    max_chars: int = MAXS_CHARS
) -> str:
    files = collect_files_fn(directory)
    file_info_lines = []
    total_chars = 0

    for file in files:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                size = len(content)
                total_chars += size
                file_info_lines.append(f"- {file} ({size} chars)")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    tree_text = tree_string_fn(directory)
    info = "\n".join(file_info_lines)

    prompt = f"""Here is the project file tree:

{tree_text}

And here are the file sizes for text files:

{info}

Which file or files should I include in a prompt to generate a good README.md for the project? If theres already a README.md or any file that looks like a note, defintely include that.
Please answer with relative paths to the filenames as this list will be loaded and used programmatically, an example:
index.html
js/main.js
"""
    print(prompt)
    return prompt

def ask_openai_for_readme_sources(
    directory: str,
    openai_client,
    collect_files_fn: Callable[[str], List[str]],
    tree_string_fn: Callable[[str], str],
    model: str = "gpt-4.1"
):
    prompt = get_tree_with_file_sizes(
        directory=directory,
        collect_files_fn=collect_files_fn,
        tree_string_fn=tree_string_fn
    )

    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
