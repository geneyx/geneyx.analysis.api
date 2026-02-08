import json
import os
import sys

# Ensure package import works when running this file directly
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from AdvancedAnalysisFileParser import AdvancedAnalysisParser

def main():
    base = os.path.join(os.path.dirname(__file__), "Test")
    filename = "dragen_4_4_4.wgs.hg38.targeted.json"
    request = {
        "input_dir": base,
        "output_dir": base,
        "output_json": "adv_output.json",
        "map_files": {
            filename: {
                "lpa": {
                    "caller_name": "LPA Caller"
                },
                "rh": {
                    "caller_name": "RH Caller"
                },
                "cyp2b6": {
                    "caller_name": "CYP2B6 Caller"
                },
                "cyp2d6": {
                    "caller_name": "CYP2D6 Caller"
                },
                "cyp21a2": {
                    "caller_name": "CYP21A2 Caller"
                },
                "smn": {
                    "caller_name": "SMN Caller",
                    "Warning": {
                        "type": "smn",
                        "disease_name": "Spinal Muscular Atrophy",
                        "silent_carrier_variant": "NM_000344.4:c.*3+80T>G",
                        "silent_carrier_min_allele_copy": 1
                    }
                },
                "gba": {
                    "caller_name": "GBA Caller",
                    "Warning": {
                        "type": "gba",
                        "disease_name": "Gaucher disease"
                    }
                },
                "hba": {
                    "caller_name": "HBA Caller",
                    "Warning": {
                        "type": "genotype",
                        "phenotypeGenotypeMapping": {
                            "normal": ["aa/aa"],
                            "silent carrier": ["-a3.7/aa", "-a4.2/aa"],
                            "carrier": ["--/aaa3.7", "--/aaa4.2", "-a3.7/-a3.7", "-a4.2/-a4.2", "-a3.7/-a4.2", "--/aa"],
                            "positive for hemoglobin H disease": ["--/-a3.7", "--/-a4.2"],
                            "positive for hemoglobin Bart's hydrops fetalis disease": ["--/--"]
                        }
                    }
                }
            }
        }
    }
    parser = AdvancedAnalysisParser(request)
    result = parser.run(return_dict=True)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
