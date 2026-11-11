from dataclasses import dataclass, asdict
from pathlib import Path
import pandas as pd


@dataclass
class CleaningLogEntry:
    step: str
    columns: str
    rule: str
    n_affected: int
    before: str
    after: str
    justification: str


class CleaningLog:
    def __init__(self):
        self.entries = []

    def add(self, step, columns, rule, n_affected, before, after, justification):
        self.entries.append(CleaningLogEntry(step, columns, rule, int(n_affected), str(before), str(after), justification))

    def to_df(self):
        if not self.entries:
            return pd.DataFrame(columns=["step", "columns", "rule", "n_affected", "before", "after", "justification"])
        return pd.DataFrame([asdict(e) for e in self.entries])

    def save(self, csv_path: Path, md_path: Path):
        df = self.to_df()
        df.to_csv(csv_path, index=False)
        md_path.write_text("# Cleaning Log\n\n" + df.to_string(index=False))
