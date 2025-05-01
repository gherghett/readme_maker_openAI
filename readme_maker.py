from openai import OpenAI
from dotenv import load_dotenv
import sys
import os
import argparse
from readme_maker import make_tree, file_collection as collector , readme_selector

# Threshold for character count
CHARACTER_LIMIT = 17_000

def get_total_character_count(file_paths):
    total_chars = 0
    for path in file_paths:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                total_chars += len(f.read())
        except Exception as e:
            print(f"Error reading {path}: {e}")
    return total_chars

def upload_files_if_small(directory):
    files = collector.collect_files(directory)
    total_chars = get_total_character_count(files)
    
    print(f"Found {len(files)} files with a total of {total_chars} characters.")

    if total_chars >= CHARACTER_LIMIT:
        print("Too much content to upload (>= 10,000 characters). Aborting.")
        return

    uploaded_ids = []
    for file in files:
        try:
            with open(file, "rb") as f:
                response = client.files.create(file=f, purpose="user_data")
                print(f"Uploaded {file} (ID: {response.id})")
                uploaded_ids.append(response.id)
        except Exception as e:
            print(f"Failed to upload {file}: {e}")

    print(f"Uploaded {len(uploaded_ids)} files.")
    return uploaded_ids

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dir", 
        default= ".",
        help="The directory to make a README.md for"
    )
    parser.add_argument(
        "-o", "--output", 
        default="README.md",
        help="Path to save the generated README (default: README.md)"
    )
    args = parser.parse_args()

    if not args.dir or not os.path.exists(args.dir):
        parser.error("The provided path is invalid.")

    tree = make_tree.tree_string(args.dir)

    # print(tree)

    # Load the .env file
    load_dotenv()

    # Get the key from environment
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in .env file")

    # Pass it into the client
    client = OpenAI(api_key=api_key)

    result = readme_selector.ask_openai_for_readme_sources(
        directory=args.dir,
        openai_client=client,
        collect_files_fn=collector.collect_files,
        tree_string_fn=make_tree.tree_string
    )

    print(result)

    selected_files = [
        os.path.join(args.dir, line.strip())
        for line in result.strip().splitlines()
        if line.strip()
    ]

    combined_content = collector.get_combined_file_content_from_list(selected_files)
    
    if combined_content:
        response = client.responses.create(
            model="gpt-4o",
            input=[
                {"role": "user", "content": f"I want you to write a README.md for this repo, here's the file structure: \n{tree}" +
                f"\n ---- \n Make it informative and brief, a good jumping of point for a simple README.md but neat and nicely formatted. " +
                # f"\n{instruction}" +
                 "\n if theres already a README.md then take whats in it to be what should be the developed into a full README.md"
                f"heres some of the project: \n {combined_content}"}
            ]
        )
        # print(response.output_text)
        output_path = os.path.join(args.dir, args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.output_text)

    else:
        print("No text was collected to send.")


