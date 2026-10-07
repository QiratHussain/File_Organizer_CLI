import argparse
from pathlib import Path

from organizer import FileOrganizer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Sort files in a directory into subfolders by type.",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(Path.home() / "Downloads"),
        help="Directory to organize (default: ~/Downloads)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without moving anything.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print a summary of categories without moving anything.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Also process hidden files (starting with '.').",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        org = FileOrganizer(
            target_dir=args.directory,
            skip_hidden=not args.include_hidden,
        )
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}")
        return

    if args.preview:
        plan = org.preview()
        print(f"\n📁 Preview for: {org.target_dir}\n")
        if not plan:
            print("  (no files found)")
        for category, files in sorted(plan.items()):
            print(f"  {category} ({len(files)}):")
            for f in files:
                print(f"    - {f}")
        print("\n(No files were moved. Use --dry-run to see the plan in action.)\n")
        return

    org.organize(dry_run=args.dry_run)


if __name__ == "__main__":
    main()