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
git clone https://github.com/geneyx/geneyx.analysis.api.git
cd geneyx.analysis.api\scripts\AdvancedAnalysisFileParser
pip install -e .
pip install pytest
pytest -s Test_AdvancedAnalysisParser.py
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

## AdvancedAnalysisFile Properties

| JSON Name | Type                               | Required? |
|-----------|------------------------------------|-----------|
| LPA       | AdvancedAnalysis<LpaData>          | No        |
| SMN1      | AdvancedAnalysis<Smn1Data>         | No        |
| SMN       | AdvancedAnalysis<SmnData>          | No        |
| HBA       | AdvancedAnalysis<HbaData>          | No        |
| RH        | AdvancedAnalysis<RhData>           | No        |
| CYP2D6    | AdvancedAnalysis<Cyp2bData>        | No        |
| CYP2B6    | AdvancedAnalysis<Cyp2bData>        | No        |
| CYP21A2   | AdvancedAnalysis<Cyp21a2Data>      | No        |
| GBA       | AdvancedAnalysis<GbaData>          | No        |
| TMB       | AdvancedAnalysis<TmbData>          | No        |
| GIS       | AdvancedAnalysis<GisData>          | No        |
| MSI       | AdvancedAnalysis<MsiData>          | No        |
| HRD       | AdvancedAnalysis<HrdData>          | No        |

---

## Common Wrapper

### AdvancedAnalysis<T>

| JSON Name | Type     | Required? |
|-----------|----------|-----------|
| data      | T        | No        |
| Warning   | string   | No        |

---

## Data Models

### LpaData

| JSON Name                   | Type               | Required? |
|-----------------------------|--------------------|-----------|
| kiv2CopyNumber              | double             | Yes       |
| refMarkerAlleleCopyNumber   | double?            | No        |
| altMarkerAlleleCopyNumber   | double?            | No        |
| type                        | LpaType            | Yes       |
| variants                    | List<Variant>      | Yes       |

---

### Smn1Data

| JSON Name            | Type    | Required? |
|----------------------|---------|-----------|
| #Sample              | string  | Yes       |
| isSMA                | bool    | Yes       |
| isCarrier            | bool    | Yes       |
| SMN1_CN              | double  | No        |
| SMN2_CN              | double  | No        |
| SMN2delta7-8_CN      | int     | Yes       |
| Total_CN_raw         | double  | Yes       |
| Full_length_CN_raw   | double  | Yes       |
| SMN1_CN_raw          | string  | Yes       |

---

### SmnData

| JSON Name            | Type            | Required? |
|----------------------|-----------------|-----------|
| smn1CopyNumber       | double?         | Yes       |
| smn2CopyNumber       | double?         | Yes       |
| smn2Delta78CopyNumber| int             | Yes       |
| totalCopyNumber      | double          | Yes       |
| fullLengthCopyNumber | double          | No        |
| variants             | List<Variant>   | Yes       |

---

### HbaData

| JSON Name         | Type              | Required? |
|-------------------|-------------------|-----------|
| genotype          | string            | Yes       |
| genotypeFilter    | GenotypeFilter    | Yes       |
| genotypeQual      | double            | Yes       |
| minPValue         | double            | Yes       |
| variants          | List<Variant>     | Yes       |

---

### RhData

| JSON Name        | Type            | Required? |
|------------------|-----------------|-----------|
| totalCopyNumber  | int             | Yes       |
| rhdCopyNumber    | int             | Yes       |
| rhceCopyNumber   | int             | Yes       |
| variants         | List<Variant>   | Yes       |

---

### Cyp2bData

| JSON Name               | Type             | Required? |
|-------------------------|------------------|-----------|
| genotype                | string           | Yes       |
| genotypeFilter          | GenotypeFilter   | Yes       |
| pharmcatDescription     | string           | No        |
| pharmcatMetabolismStatus| string           | No        |

---

### Cyp21a2Data

| JSON Name                | Type            | Required? |
|--------------------------|-----------------|-----------|
| totalCopyNumber          | int             | Yes       |
| deletionBreakpointInGene | bool?           | No        |
| recombinantHaplotypes    | List<string>    | No        |
| variants                 | List<Variant>   | Yes       |

---

### GbaData

| JSON Name                      | Type    | Required? |
|--------------------------------|---------|-----------|
| #Sample                        | string  | Yes       |
| is_biallelic                   | bool    | Yes       |
| is_carrier                     | bool    | Yes       |
| total_CN                       | int     | Yes       |
| deletion_breakpoint_in_GBA_gene| string  | No        |
| recombinant_variants           | string  | No        |
| other_variants                 | string  | No        |

---

### TmbData

| JSON Name   | Type   | Required? |
|-------------|--------|-----------|
| Total TMB   | double | Yes       |

---

### GisData

| JSON Name                | Type    | Required? |
|--------------------------|---------|-----------|
| Genomic Instability Score| int     | No        |
| Tumor Fraction           | double  | No        |
| Ploidy                   | double  | No        |

---

### MsiData

| JSON Name                  | Type    | Required? |
|----------------------------|---------|-----------|
| Percent Unstable MSI Sites | double  | Yes       |

---

### HrdData

| JSON Name   | Type   | Required? |
|-------------|--------|-----------|
| HRD Score   | int    | Yes       |

---

### Variant

| JSON Name            | Type    | Required? |
|----------------------|---------|-----------|
| hgvs                 | string  | No        |
| qual                 | double  | No        |
| altCopyNumber        | int     | No        |
| altCopyNumberQuality | double  | No        |

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


