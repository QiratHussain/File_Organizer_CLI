# 🗂️ File Organizer

A command-line tool that automatically sorts a messy directory (like `~/Downloads`)
into subfolders by file type: Documents, Images, Videos, Audio, Archives, Code.

Built with **only the Python standard library** — no external dependencies for the
core tool.

## Features

- 🔍 **Preview mode** — see what will happen before anything moves
- 🧪 **Dry-run mode** — log the plan safely
- 🛡️ **Safe renames** — duplicate filenames get `_1`, `_2` suffixes (nothing overwritten)
- 🧾 **Logging** — timestamped output via Python's `logging` module
- ⚙️ **Configurable rules** — extensions are mapped in one place (`rules.py`)
- ✅ **Unit tested** with `pytest`

## Installation

```bash
git clone https://github.com/yourname/file-organizer
cd file-organizer
pip install -r requirements.txt
```

## Usage

```bash
# See how files would be categorized (nothing is moved)
python main.py ~/Downloads --preview

# Dry-run — logs each planned move
python main.py ~/Downloads --dry-run

# Actually organize
python main.py ~/Downloads
```

## Example

Before:

```
Downloads/
├── resume.pdf
├── cat.jpg
├── song.mp3
├── notes.txt
└── script.py
```

After running `python main.py ~/Downloads`:

```
Downloads/
├── Documents/    → resume.pdf, notes.txt
├── Images/       → cat.jpg
├── Audio/        → song.mp3
└── Code/         → script.py
```

## Running tests

```bash
pytest -v
```

## Project structure

```
organizer/       → the actual tool (a proper Python package)
  ├── organizer.py   (FileOrganizer class)
  ├── rules.py       (extension → category map)
  └── logger.py      (logging configuration)
main.py          → CLI entry point using argparse
tests/           → pytest unit tests
```

## What I learned building this

- Designing a small Python package with clean module boundaries
- Using `pathlib` instead of `os.path` for file operations
- Safe file moves with `shutil.move` and duplicate handling
- Building a real CLI with `argparse` (subcommand-style flags)
- Writing unit tests with `pytest` and `tmp_path` fixtures
- Using `logging` instead of `print()` in a real tool