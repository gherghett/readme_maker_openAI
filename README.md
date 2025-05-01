# README Maker

This is a fun project, a CLI-tool to generate a `README.md` for a programming project using OpenAI's API. It analyzes the file structure and content to produce a neatly formatted and informative readme.

This README.md was made with readme_maker (but also manually fixed)

## Features

- Generates `README.md` using OpenAI's API.
- Scans directory structure and file content.
- Integrates `.gitignore` to exclude specified files.
- Provides CLI for ease of use.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/gherghett/readme_maker_openAI/
   cd readme_maker_openAI
   ```

2. **Install dependencies:**

   Make sure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Environment Setup:**

   - Create a `.env` file in the root directory.
   - Add your OpenAI API key to the `.env`:

     ```env
     OPENAI_API_KEY='your_api_key_here'
     ```

2. **Generate a README:**

   Use the CLI to generate a `README.md`:

   ```bash
   python readme_maker.py -d <directory-path> -o <output-path>
   ```

   - `-d` or `--dir`: Specifies the directory for which to generate the README.
   - `-o` or `--output`: Specifies the output file path for the generated README.

## Project Structure

- **readme_maker.py**: Main script that automates README generation.
  - Scans the target folder and builds a representation of its contents.
  - Sends this representation to OpenAI to request suggested README content.
  - Gathers relevant text files, concatenates them, and includes them in the prompt.
  - Writes the generated README to the specified output location.  
  - *Note: The generated results are often underwhelming.*
- **readme_maker**: Module responsible for file and tree operations.
  - `file_collection.py`: Manages file collection and content aggregation.
  - `make_tree.py`: Generates a visual tree of the directory structure.
  - `readme_selector.py`: Interface with OpenAI to select relevant content for README.

## Contributing

Feel free to fork the project, open issues, or submit pull requests. Contributions are welcome! Steal it whatever.

## License

This project does not have a specific license yet, so assume it is not open source until otherwise specified. But its not closed until otherwise sworn. Its mostly AI-genereated.

-----

Enjoy using README Maker!
