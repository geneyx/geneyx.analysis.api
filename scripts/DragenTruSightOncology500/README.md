## Overview

This project automates the extraction of TSV output from the DRAGEN TruSight Oncology 500 pipeline to JSON for `UploadAdvanceAnalysisToSample` endpoint.

The provided Python script:

* Parses a TSV report, extracting key/value and table sections.
* Applies configurable filters and warning thresholds per section.
* Outputs a JSON payload ready for HTTP pre/post requests.

## Prerequisites

* Python 3.7+

## Repository Structure

```
├── DragenTruSightOncology500TSVParser.py           # TSV parsing logic
├── sample_ID__CombinedVariantOutput.tsv            # Example TSV from DRAGEN oncology
└── README.md                                       # This documentation
```

## Configuration

In `DragenTruSightOncology500TSVParser.py`, adjust `sections_to_parse` to match your sections and warning thresholds:

```python
sections_to_parse = {
    "msi": SectionConfig(
        fields={
            "Percent Unstable MSI Sites": FieldConfig(
                warning=FieldWarning(threshold=10, warning="MSI>10 detected")
            )
        }
    ),
    "tmb": SectionConfig(
        fields={
            "Total TMB": FieldConfig(
                warning=FieldWarning(threshold=10, warning="TMB>10 detected")
            )
        }
    ),
    "gis": SectionConfig(
        include_all_fields=True,
        fields={
            "Genomic Instability Score": FieldConfig(
                warning=FieldWarning(threshold=42, warning="GIS>42 detected")
            )
        }
    )
}
```

## Generating `form-data` JSON

Run the parser to convert your TSV into JSON:

```bash
python DragenTruSightOncology500TSVParser.py --input sample_report.tsv --output payload.json
```

This command will produce `payload.json` with the structure:

```json
{
    "msi": {
        "data": { /* key/value pairs */ },
        "Warning": "..."
    },
    "tmb": { ... },
    "gis": [
        { "data": {...}, "Warning": "..." },
        ...
    ]
}
```

## API: `UploadAdvanceAnalysisToSample`

* **Endpoint**: `POST /api/samples/{sampleId}/advance-analysis`
* **Content-Type**: `application/json` or `multipart/form-data`

On success, you’ll receive HTTP `200 OK` with the saved analysis record.

## Automating the Workflow

You can combine parsing and upload in a single Python script:

```python
import json
import requests
from parser import DragenTruSightOncology500TSVParser

# Parse TSV
parser = DragenTruSightOncology500TSVParser('sample_report.tsv')
payload = parser.parse_tsv(sections_to_parse)

```

## Contributing
Bar Cohen

### **Additional Help & Support**:
For any troubleshooting or questions, feel free to contact [support@geneyx.com](mailto:support@geneyx.com).

## License

Copyright (c) 2025 GeneyX Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

