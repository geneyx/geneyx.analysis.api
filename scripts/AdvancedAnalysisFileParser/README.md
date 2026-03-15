

# Advanced Analysis Parser

This project now uses the [AdvancedAnalysisFileParser](https://pypi.org/project/AdvancedAnalysisFileParser/) package.

## Installation

```bash
pip install AdvancedAnalysisFileParser==0.1.2
```

## Quickstart

### In-Memory Usage

```python
import os
from AdvancedAnalysisFileParser import JsonDict, AdvancedAnalysisParser

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "Test")
request: JsonDict = {
    "output_json": "out.json",
    "input_dir": TEST_DATA_DIR,
    "input_files": [
        "test.gba.tsv",
        "test.smn.tsv",
        "test.wgs.hg38.targeted.json",
        "TruSightOncology500\\sample_ID__CombinedVariantOutput.tsv"
    ]
}

parser = AdvancedAnalysisParser(request)
result = parser.run()
```
### Running Tests

To run the test suite:

```bash
pytest scripts/AdvancedAnalysisFileParser/test_advanced_analysis_parser.py
```

Make sure your test data files are in `scripts/AdvancedAnalysisFileParser/Test/`.

### Command-Line Usage

1. Create a config file, e.g. `config.json` (see above).
2. Run:

   ```bash
   python -m AdvancedAnalysisFileParser -c config.json
   ```

This will write the unified JSON to `output_json` under `input_dir`.

---

## Features

* Unified JSON output across multiple callers
* Plug-and-play parser for TSV & JSON formats
* Built-in pytest suite for validation

---

## Contributing

1. Fork
2. Create feature branch
3. Submit PR

For troubleshooting or questions, contact [support@geneyx.com](mailto:support@geneyx.com).

## License

Copyright (c) 2025 GeneyX. See LICENSE for details.
```


