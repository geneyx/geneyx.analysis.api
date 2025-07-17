# Advanced Analysis Parser

A Python utility to parse Illumina-DRAGEN “special caller” outputs (TSV or JSON) into a unified JSON format, with per-field warnings based on user-defined conditions.

---

## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Quickstart](#quickstart)

  * [In-Memory Usage](#in-memory-usage)
  * [Command-Line Usage](#command-line-usage)
* [Configuration JSON](#configuration-json)

  * [Top-Level Keys](#top-level-keys)
  * [`map_files` Structure](#map_files-structure)

    * [TSV Caller Example (MSI/TMB/GIS)](#tsv-caller-example-msi-tmb-gis)
    * [Boolean-Flag Caller Example (GBA/SMN)](#boolean-flag-caller-example-gbasmn)
    * [Genotype-Mapping Example (HBA)](#genotype-mapping-example-hba)
* [Warning Types](#warning-types)

  * [`condition`](#condition)
  * [`genotype`](#genotype)
* [Running Tests](#running-tests)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* Unified JSON output across multiple callers
* Per-field or per-caller warnings driven by JSON-defined conditions
* Pluggable parser implementations for TSV & JSON formats
* Built-in pytest suite for validation

---

## Installation

```bash
git clone https://github.com/your-org/advanced-analysis-parser.git
cd advanced-analysis-parser
pip install -e .
```

---

## Quickstart

### In-Memory Usage

```python
from AdvancedAnalysisFileParser import AdvancedAnalysisParser, JsonDict

# Build your JSON request (see next section for details)
request: JsonDict = {
    "output_json": "out.json",
    "input_dir": "path/to/input",
    "map_files": {
        "MyCallerOutput.tsv": {
            "MY_CALLER": {
                "caller_name": "My Caller",
                "fields": { ... },
            }
        }
    }
}

parser = AdvancedAnalysisParser(request)
result = parser.run(return_dict=True)
print(result)
```

### Command-Line Usage

1. Create a config file, e.g. `config.json` (see below).
2. Run:

   ```bash
   python -m advanced_analysis_parser -c config.json
   ```

This will write the unified JSON to `output_json` under `input_dir`.

---

## Configuration JSON

Your top‐level JSON must include:

| Key           | Type   | Description                                                           |
| ------------- | ------ | --------------------------------------------------------------------- |
| `output_json` | string | Filename for the generated JSON (default: `adv_analysis_output.json`) |
| `input_dir`   | string | Directory containing all input files                                  |
| `map_files`   | object | Mapping of filenames → caller definitions                             |

### `map_files` Structure

```jsonc
"map_files": {
  "<filename.tsv|.json>": {
    "<CALLER_KEY>": {
      "caller_name": "<Human-readable name>",

      // Option A: per-field warnings
      "fields": {
        "<FieldName>": {
          "Warning": {
            "type": "condition",
            "conditions": [
              {
                "operator": "GT",
                "value": 10,
                "message": "Value > 10"
              }
            ]
          }
        }
      }

      // Option B: whole-caller warning (no "fields" key)
      "Warning": {
        "type": "condition",
        "conditions": [ ... ]
      }
    },
    /* repeat for other callers in the same file */
  }
}
```

#### TSV Caller Example (MSI/TMB/GIS)

```json
{
  "TruSightOncology500\\sample__CombinedVariantOutput.tsv": {
    "MSI": {
      "caller_name": "Percent Unstable MSI Sites",
      "fields": {
        "Usable MSI Sites": {
          "Warning": {
            "type": "condition",
            "conditions": [
              { "operator": "GT", "value": 10, "message": "MSI>10 detected" }
            ]
          }
        }
      }
    },
    "TMB": {
      "caller_name": "Total TMB",
      "fields": {
        "Total TMB": {
          "Warning": {
            "type": "condition",
            "conditions": [
              { "operator": "GT", "value": 10, "message": "TMB>10 detected" }
            ]
          }
        }
      }
    },
    "GIS": {
      "caller_name": "Genomic Instability Score",
      "fields": {
        "Genomic Instability Score": {
          "Warning": {
            "type": "condition",
            "conditions": [
              { "operator": "GT", "value": 42, "message": "GIS>42 detected" }
            ]
          }
        }
      }
    }
  }
}
```

#### Boolean-Flag Caller Example (GBA/SMN)

```json
{
  "SRR1289…gba.tsv": {
    "GBA": {
      "caller_name": "GBA Special Caller",
      "Warning": {
        "type": "condition",
        "disease_name": "Gaucher disease",
        "conditions": [
          {
            "field": "is_carrier",
            "operator": "EQ",
            "value": true,
            "message": "Carrier positive for Gaucher disease"
          },
          {
            "field": "is_biallelic",
            "operator": "EQ",
            "value": true,
            "message": "Carrier positive for Gaucher disease"
          }
        ]
      }
    }
  }
}
```

#### Genotype-Mapping Example (HBA)

```json
{
  "…targeted.json": {
    "hba": {
      "caller_name": "HBA Special Caller",
      "Warning": {
        "type": "genotype",
        "phenotypeGenotypeMapping": {
          "silent carrier": [
            "-a3.7/aa", "-a4.2/aa"
          ],
          "carrier": [
            "--/aaa3.7", "--/aaa4.2"
          ],
          "positive for hemoglobin H disease": [
            "--/-a3.7","--/-a4.2"
          ]
        }
      }
    }
  }
}
```

---

## Warning Types

### `condition`

* Evaluates one or more **FieldCondition** entries
* Each condition must specify:

  * `field` (optional for per-field; required for whole-caller)
  * `operator`: one of `EQ`, `NE`, `GT`, `LT`, etc.
    * `EQ`: Equals (`a == b`)
    * `NE`: Not Equals (`a != b`)
    * `GT`: Greater then (`a > b`)
    * `LT`: Less then (`a < b`)
    * `GE`: Greater then or equal (`a >= b`)
    * `LE`: Less then or equal (`a <= b`)
    * `CONTAINS`: Equals (`b in a`)
  * `value`: comparison target
  * `message`: text to emit if triggered

### `genotype`

* Maps raw genotypes → phenotype labels
* First matching genotype string in `phenotypeGenotypeMapping` is used

---

## Running Tests

We use `pytest` and parametrize via in-memory JSON contexts.

```bash
pip install pytest
pytest tests/
```

Sample snippet from `tests/test_parser.py`:

```python
import pytest
from AdvancedAnalysisFileParser import JsonDict, AdvancedAnalysisParser

TEST_CONTEXTS = [ { "request": { … }, "expected": { … } } ]

@pytest.mark.parametrize("context", TEST_CONTEXTS)
def test_parser_in_memory(context: JsonDict):
    parser = AdvancedAnalysisParser(context["request"])
    result = parser.run(return_dict=True)
    assert result["MSI"]["warning"] == "MSI>10 detected"
    # … more assertions …
```

---
---

## AdvancedAnalysisFile Properties

| Property Name | Type                               | Required? |
|---------------|------------------------------------|-----------|
| Lpa           | AdvancedAnalysis<LpaData>          | No        |
| Smn1          | AdvancedAnalysis<Smn1Data>         | No        |
| Smn           | AdvancedAnalysis<SmnData>          | No        |
| Hba           | AdvancedAnalysis<HbaData>          | No        |
| Rh            | AdvancedAnalysis<RhData>           | No        |
| Cyp2d6        | AdvancedAnalysis<Cyp2bData>        | No        |
| Cyp2b6        | AdvancedAnalysis<Cyp2bData>        | No        |
| Cyp21a2       | AdvancedAnalysis<Cyp21a2Data>      | No        |
| Gba           | AdvancedAnalysis<GbaData>          | No        |
| Tmb           | AdvancedAnalysis<TmbData>          | No        |
| Gis           | AdvancedAnalysis<GisData>          | No        |
| Msi           | AdvancedAnalysis<MsiData>          | No        |
| Hrd           | AdvancedAnalysis<HrdData>          | No        |

---

## Common Wrapper

### AdvancedAnalysis<T>

| Property Name | Type     | Required? |
|---------------|----------|-----------|
| Data          | T        | No        |
| Warning       | string   | No        |

---

## Data Models

### LpaData

| Property Name                | Type               | Required? |
|------------------------------|--------------------|-----------|
| Kiv2CopyNumber               | double             | Yes       |
| RefMarkerAlleleCopyNumber    | double?            | No        |
| AltMarkerAlleleCopyNumber    | double?            | No        |
| Type                         | LpaType            | Yes       |
| Variants                     | List<Variant>      | Yes       |

---
### Smn1Data

| Property Name    | Type    | Required? |
|------------------|---------|-----------|
| Sample           | string  | Yes       |
| IsSma            | bool    | Yes       |
| IsCarrier        | bool    | Yes       |
| Smn1Cn           | double  | No        |
| Smn2Cn           | double  | No        |
| Smn2delta78Cn    | int     | Yes       |
| TotalCnRaw       | double  | Yes       |
| FullLengthCnRaw  | double  | Yes       |
| Smn1CnRaw        | string  | Yes       |

---

### SmnData

| Property Name      | Type            | Required? |
|--------------------|-----------------|-----------|
| Smn1Cn             | double?         | Yes       |
| Smn2Cn             | double?         | Yes       |
| Smn2delta78Cn      | int             | Yes       |
| TotalCnRaw         | double          | Yes       |
| FullLengthCnRaw    | double          | No        |
| Variants           | List<Variant>   | Yes       |

---

### HbaData

| Property Name    | Type              | Required? |
|------------------|-------------------|-----------|
| Genotype         | string            | Yes       |
| GenotypeFilter   | GenotypeFilter    | Yes       |
| GenotypeQual     | double            | Yes       |
| MinPValue        | double            | Yes       |
| Variants         | List<Variant>     | Yes       |

---

### RhData

| Property Name     | Type            | Required? |
|-------------------|-----------------|-----------|
| TotalCopyNumber   | int             | Yes       |
| RhdCopyNumber     | int             | Yes       |
| RhceCopyNumber    | int             | Yes       |
| Variants          | List<Variant>   | Yes       |

---

### Cyp2bData

| Property Name              | Type             | Required? |
|----------------------------|------------------|-----------|
| Genotype                   | string           | Yes       |
| GenotypeFilter             | GenotypeFilter   | Yes       |
| PharmcatDescription        | string           | No        |
| PharmcatMetabolismStatus   | string           | No        |

---

### Cyp21a2Data

| Property Name                | Type            | Required? |
|------------------------------|-----------------|-----------|
| TotalCopyNumber              | int             | Yes       |
| DeletionBreakpointInGene     | bool?           | No        |
| RecombinantHaplotypes        | List<string>    | No        |
| Variants                     | List<Variant>   | Yes       |

---

### GbaData

| Property Name                  | Type    | Required? |
|--------------------------------|---------|-----------|
| Sample                         | string  | Yes       |
| IsBiallelic                    | bool    | Yes       |
| IsCarrier                      | bool    | Yes       |
| TotalCn                        | int     | Yes       |
| DeletionBreakpointInGbaGene    | string  | No        |
| RecombinantVariants            | string  | No        |
| OtherVariants                  | string  | No        |

---

### TmbData

| Property Name   | Type   | Required? |
|-----------------|--------|-----------|
| Total           | double | Yes       |

---

### GisData

| Property Name     | Type    | Required? |
|-------------------|---------|-----------|
| Instability       | int     | No        |
| TumorFraction     | double  | No        |
| Ploidy            | double  | No        |

---

### MsiData

| Property Name           | Type    | Required? |
|-------------------------|---------|-----------|
| UnstableMsiSitePercent  | double  | Yes       |

---

### HrdData

| Property Name   | Type   | Required? |
|-----------------|--------|-----------|
| Score           | int    | Yes       |

---

### Variant

| Property Name         | Type    | Required? |
|-----------------------|---------|-----------|
| Hgvs                  | string  | No        |
| Qual                  | double  | No        |
| AltCopyNumber         | int     | No        |
| AltCopyNumberQuality  | double  | No        |

---

## Contributing

1. Fork
2. Create feature branch
3. Submit PR

Please follow existing style and add tests for new parser logic.
Bar Cohen

### **Additional Help & Support**:
For any troubleshooting or questions, feel free to contact [support@geneyx.com](mailto:support@geneyx.com).

## License

Copyright (c) 2025 GeneyX Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```


