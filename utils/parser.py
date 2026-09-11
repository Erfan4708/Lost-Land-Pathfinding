# parser.py: Reads the example maps from a text file.

from typing import Any, List, Tuple

from config import THIEF


class MapParser:
    """
    Reads maps written as plain text. A map starts with a line such as
    "Example1" and is followed by its rows, one row per line, with the cell
    values separated by spaces.
    """

    @staticmethod
    def parse_examples_from_file(file_path: str) -> List[Tuple[str, List[List[Any]]]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        examples = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1

            if not line.startswith("Example"):
                continue

            example_name = line
            grid = []

            while i < len(lines):
                row_line = lines[i].strip()
                if not row_line or row_line.startswith("Example"):
                    break
                grid.append(MapParser._parse_row(row_line, example_name))
                i += 1

            examples.append((example_name, grid))

        return examples

    @staticmethod
    def _parse_row(row_line: str, example_name: str) -> List[Any]:
        row = []
        for token in row_line.split():
            if token == THIEF:
                row.append(THIEF)
            else:
                try:
                    row.append(int(token))
                except ValueError:
                    raise ValueError(
                        f"Invalid cell {token!r} in {example_name}: "
                        f"a cell must be a whole number or {THIEF!r}"
                    ) from None
        return row
