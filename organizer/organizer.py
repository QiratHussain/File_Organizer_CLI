from pathlib import Path
from datetime import datetime
import shutil

from .rules import get_category
from .logger import setup_logger


class FileOrganizer:

    def __init__(self, target_dir: Path, skip_hidden: bool = True):
        self.target_dir = Path(target_dir).expanduser().resolve()
        self.skip_hidden = skip_hidden
        self.logger = setup_logger()

        if not self.target_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.target_dir}")
        if not self.target_dir.is_dir():
            raise NotADirectoryError(f"Not a directory: {self.target_dir}")

    # ---------- Discovery ----------
    def scan(self):
        """Return a list of files (not folders) in the target directory."""
        files = []
        for item in self.target_dir.iterdir():
            if not item.is_file():
                continue
            if self.skip_hidden and item.name.startswith("."):
                continue
            files.append(item)

        self.logger.info(f"Found {len(files)} file(s) in {self.target_dir}")
        return files

    # ---------- Core action ----------
    def organize(self, dry_run: bool = False) -> dict:
        """
        Move files into category folders.

        Returns a summary dict:
            {
                "moved": [(src, dest), ...],
                "skipped": [(path, reason), ...],
                "dry_run": bool,
            }
        """
        files = self.scan()
        summary = {"moved": [], "skipped": [], "dry_run": dry_run}

        if not files:
            self.logger.info("Nothing to do.")
            return summary

        for file in files:
            try:
                destination = self._destination_for(file)
                summary["moved"].append((file, destination))

                if dry_run:
                    self.logger.info(f"[DRY-RUN] {file.name} → {destination.parent.name}/")
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination = self._unique_path(destination)
                    shutil.move(str(file), str(destination))
                    self.logger.info(f"Moved: {file.name} → {destination.parent.name}/")

            except PermissionError:
                reason = "Permission denied"
                summary["skipped"].append((file, reason))
                self.logger.warning(f"Skipped {file.name}: {reason}")

            except Exception as e:
                summary["skipped"].append((file, str(e)))
                self.logger.error(f"Error with {file.name}: {e}")

        self._log_summary(summary)
        return summary

    # ---------- Helpers ----------
    def _destination_for(self, file: Path) -> Path:
        """Return the full destination path for a file."""
        category = get_category(file.suffix)
        return self.target_dir / category / file.name

    def _unique_path(self, path: Path) -> Path:
        """If a file with that name exists, add a numeric suffix."""
        if not path.exists():
            return path

        stem, suffix = path.stem, path.suffix
        counter = 1
        while True:
            new_path = path.with_name(f"{stem}_{counter}{suffix}")
            if not new_path.exists():
                return new_path
            counter += 1

    def _log_summary(self, summary: dict) -> None:
        mode = "DRY-RUN" if summary["dry_run"] else "DONE"
        self.logger.info(
            f"[{mode}] Moved {len(summary['moved'])}, "
            f"skipped {len(summary['skipped'])}"
        )

    # ---------- Info ----------
    def preview(self) -> dict:
        """Return a dict: {category: [filenames]} without moving anything."""
        plan = {}
        for file in self.scan():
            category = get_category(file.suffix)
            plan.setdefault(category, []).append(file.name)
        return plan

    def __repr__(self) -> str:
        return f"FileOrganizer(target_dir='{self.target_dir}')"