# Q2 Cleaning Log

The Q2 cleaning function strips whitespace, maps category variants, converts numeric text with commas or units, invalidates implausible values, removes duplicate records, and drops rows without an identifiable target. Counts are produced when `03_clean.ipynb` runs.

The raw synthetic fixture is never edited. Any result based on it must be labelled synthetic test output.