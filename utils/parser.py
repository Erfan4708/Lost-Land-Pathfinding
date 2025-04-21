from typing import List, Tuple, Union
from config import THIEF

class MapParser:
    @staticmethod
    def parse_examples_from_file(file_path: str) -> List[Tuple[str, List[List[Union[int, str]]]]]:
        examples = []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            if line.startswith("Example"):
                example_name = line
                i += 1
                grid = []

                while i < len(lines):
                    row_line = lines[i].strip()
                    if not row_line or row_line.startswith("Example"):
                        break

                    row = []
                    for token in row_line.split():
                        if token == "!":
                            row.append(THIEF)
                        else:
                            row.append(int(token))
                    grid.append(row)
                    i += 1

                examples.append((example_name, grid))
                continue

            i += 1

        return examples
