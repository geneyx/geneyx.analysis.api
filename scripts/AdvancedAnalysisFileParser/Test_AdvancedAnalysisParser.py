import json
import logging
import pytest
from AdvancedAnalysisFileParser import JsonDict
from AdvancedAnalysisFileParser import AdvancedAnalysisParser
# Define test contexts for parametrization
TEST_CONTEXTS = [
    {
        "request": {
            "output_json": "out.json",
            "input_dir": "Test",
            "map_files": {
                "TruSightOncology500\\sample_ID__CombinedVariantOutput.tsv":{
                    "MSI": {
                        "caller_name": "Percent Unstable MSI Sites",
                        "fields":{
                            "Usable MSI Sites":{
                                "Warning":{
                                    "type": "condition",
                                    "conditions":[
                                        {
                                            "operator": "GT",
                                            "value": 10,
                                            "message": "MSI>10 detected in this sample"
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    "TMB": {
                        "caller_name": "Total TMB",
                        "fields":{
                            "Total TMB":{
                                "Warning":{
                                    "type": "condition",
                                    "conditions":[
                                        {
                                            "operator": "GT",
                                            "value": 10,
                                            "message": "TMB>10 detected in this sample"
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    "GIS": {
                        "caller_name": "Genomic Instability Score",
                        "fields":{
                            "Genomic Instability Score":{
                                "Warning": {
                                    "type": "condition",
                                    "conditions": [
                                        {
                                            "operator": "GT",
                                            "value": 42,
                                            "message": "GIS>42 detected in this sample"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                },
                "SRR12898317_.dragen.wgs.hg38.20240705-133604.gba.tsv": {
                    # https://support-docs.illumina.com/SW/dragen_v42/Content/SW/DRAGEN/GBA_Caller.htm
                    "GBA": {
                        "caller_name": "GBA Special Caller",
                        "Warning": {
                            "type": "condition",
                            "disease_name": "Gaucher disease",
                            "conditions": [
                                { #Presence of a recombinant-like variant on only one chromosome
                                    "field": "is_carrier",
                                    "value": True,
                                    "operator": "EQ",
                                    "message": "Carrier positive for Gaucher disease",
                                },
                                { #Presence of a recombinant-like variant on each chromosome (homozygous variant or compound heterozygous)
                                    "field": "is_biallelic",
                                    "value": True,
                                    "operator": "EQ",
                                    "message": "Carrier positive for Gaucher disease",
                                }
                            ]
                        }
                    }
                },
                "SRR12898317_.dragen.wgs.hg38.20240705-133604.smn.tsv": {
                    #https://support-docs.illumina.com/SW/DRAGEN_v39/Content/SW/DRAGEN/SMNCaller.htm
                    "SMN1": {
                        "caller_name": "SMN Special Caller",
                        "Warning": {
                            "type": "condition",
                            "disease_name": "Spinal Muscular Atrophy",
                            "conditions": [
                                { # SMA affected status
                                    "field": "isSMA",
                                    "value": True,
                                    "operator": "EQ",
                                    "message": "Carrier positive for Spinal Muscular Atrophy",
                                },
                                { # SMA carrier status
                                    "field": "isCarrier",
                                    "value": True,
                                    "operator": "EQ",
                                    "message": "Carrier positive for Spinal Muscular Atrophy",
                                }
                            ]
                        }
                    }
                },
                "SRR12898317_.dragen.wgs.hg38.20240705-133604.targeted.json" :{
                    #https://help.dragen.illumina.com/product-guides/dragen-v4.3/dragen-dna-pipeline/targeted-caller/gba-calling
                    "gba" :{
                        "caller_name": "GBA Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "recombinantHaplotypes",
                                    "operator": "CONTAINS",
                                    "value": "L483P",
                                    "message": "Based on the GBA Caller, this sample is carrier for Gaucher disease"
                                }
                            ]
                        }
                    },
                    #https://help.dragen.illumina.com/product-guides/dragen-v4.3/dragen-dna-pipeline/targeted-caller/smn-calling
                    "smn": { },
                    #https://help.dragen.illumina.com/product-guides/dragen-v4.3/dragen-dna-pipeline/targeted-caller/lpa-calling
                    "lpa": { },
                    #https://help.dragen.illumina.com/product-guides/dragen-v4.3/dragen-dna-pipeline/targeted-caller/rh-calling
                    "rh": { },
                    #https://help.dragen.illumina.com/product-guides/dragen-v4.3/dragen-dna-pipeline/targeted-caller/cyp2b6-calling
                    "cyp2b6": { },
                    #https://help.dragen.illumina.com/product-guides/dragen-v4.3/dragen-dna-pipeline/targeted-caller/cyp2c19-calling
                    "cyp2d6": { },
                    #https://help.dragen.illumina.com/product-guides/dragen-v4.3/dragen-dna-pipeline/targeted-caller/cyp2c19-calling
                    "cyp21a2": { },
                    #https://help.dragen.illumina.com/product-guides/dragen-v4.3/dragen-dna-pipeline/targeted-caller/hba-calling
                    "hba": {
                        "caller_name": "HBA Special Caller",
                        "Warning": {
                            "type": "genotype",
                            "phenotypeGenotypeMapping": {
                                "alpha-globin triplication":[
                                    "aaa3.7/aa",
                                    "aaa4.2/aa",
                                    "aaa20.5/aa"
                                ],
                                "normal":[
                                    "aa/aa"
                                ],
                                "silent carrier": [
                                    "-a3.7/aa",
                                    "-a4.2/aa",
                                    "-a20.5/aa"
                                ],
                                "carrier": [
                                    "--/aaa3.7",
                                    "--/aaa4.2",
                                    "-a3.7/-a3.7",
                                    "-a4.2/-a4.2",
                                    "-a3.7/-a4.2",
                                    "--/aa",
                                    "-a20.5/-a20.5",
                                    "-a20.5/-a3.7",
                                    "-a20.5/-a4.2",
                                    "--/aaa20.5",
                                ],
                                 #Hb H disease
                                "positive for hemoglobin H disease": [
                                    "--/-a3.7",
                                    "--/-a4.2",
                                    "--/-a20.5"
                                ],
                                #Hb Bart's hydrops fetalis disease
                                "positive for hemoglobin Bart's hydrops fetalis disease": [
                                    "--/--"
                                ]
                            }
                        }
                    }
                },
                "hba_hemoglobin_h_disease.json": {
                    "hba": {
                        "caller_name": "HBA Special Caller",
                        "Warning": {
                            "type": "genotype",
                            "phenotypeGenotypeMapping": {
                                "alpha-globin triplication":[
                                    "aaa3.7/aa",
                                    "aaa4.2/aa",
                                    "aaa20.5/aa"
                                ],
                                "normal":[
                                    "aa/aa"
                                ],
                                "silent carrier": [
                                    "-a3.7/aa",
                                    "-a4.2/aa",
                                    "-a20.5/aa"
                                ],
                                "carrier": [
                                    "--/aaa3.7",
                                    "--/aaa4.2",
                                    "-a3.7/-a3.7",
                                    "-a4.2/-a4.2",
                                    "-a3.7/-a4.2",
                                    "--/aa",
                                    "-a20.5/-a20.5",
                                    "-a20.5/-a3.7",
                                    "-a20.5/-a4.2",
                                    "--/aaa20.5",
                                ],
                                 #Hb H disease
                                "positive for hemoglobin H disease": [
                                    "--/-a3.7",
                                    "--/-a4.2",
                                    "--/-a20.5"
                                ],
                                #Hb Bart's hydrops fetalis disease
                                "positive for hemoglobin Bart's hydrops fetalis disease": [
                                    "--/--"
                                ]
                            }
                        }
                    },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "hba_carrier_1.json": {
                    "hba": {
                        "caller_name": "HBA Special Caller",
                        "Warning": {
                            "type": "genotype",
                            "phenotypeGenotypeMapping": {
                                "alpha-globin triplication":[
                                    "aaa3.7/aa",
                                    "aaa4.2/aa",
                                    "aaa20.5/aa"
                                ],
                                "normal":[
                                    "aa/aa"
                                ],
                                "silent carrier": [
                                    "-a3.7/aa",
                                    "-a4.2/aa",
                                    "-a20.5/aa"
                                ],
                                "carrier": [
                                    "--/aaa3.7",
                                    "--/aaa4.2",
                                    "-a3.7/-a3.7",
                                    "-a4.2/-a4.2",
                                    "-a3.7/-a4.2",
                                    "--/aa",
                                    "-a20.5/-a20.5",
                                    "-a20.5/-a3.7",
                                    "-a20.5/-a4.2",
                                    "--/aaa20.5",
                                ],
                                 #Hb H disease
                                "positive for hemoglobin H disease": [
                                    "--/-a3.7",
                                    "--/-a4.2",
                                    "--/-a20.5"
                                ],
                                #Hb Bart's hydrops fetalis disease
                                "positive for hemoglobin Bart's hydrops fetalis disease": [
                                    "--/--"
                                ]                            }
                        }
                    },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "hba_carrier_2.json": {
                    "hba": {
                        "caller_name": "HBA Special Caller",
                        "Warning": {
                            "type": "genotype",
                            "phenotypeGenotypeMapping": {
                                "alpha-globin triplication":[
                                    "aaa3.7/aa",
                                    "aaa4.2/aa",
                                    "aaa20.5/aa"
                                ],
                                "normal":[
                                    "aa/aa"
                                ],
                                "silent carrier": [
                                    "-a3.7/aa",
                                    "-a4.2/aa",
                                    "-a20.5/aa"
                                ],
                                "carrier": [
                                    "--/aaa3.7",
                                    "--/aaa4.2",
                                    "-a3.7/-a3.7",
                                    "-a4.2/-a4.2",
                                    "-a3.7/-a4.2",
                                    "--/aa",
                                    "-a20.5/-a20.5",
                                    "-a20.5/-a3.7",
                                    "-a20.5/-a4.2",
                                    "--/aaa20.5",
                                ],
                                 #Hb H disease
                                "positive for hemoglobin H disease": [
                                    "--/-a3.7",
                                    "--/-a4.2",
                                    "--/-a20.5"
                                ],
                                #Hb Bart's hydrops fetalis disease
                                "positive for hemoglobin Bart's hydrops fetalis disease": [
                                    "--/--"
                                ]                            }
                        }
                    },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "hba_carrier_3.json": {
                    "hba": {
                        "caller_name": "HBA Special Caller",
                        "Warning": {
                            "type": "genotype",
                            "phenotypeGenotypeMapping": {
                                "alpha-globin triplication":[
                                    "aaa3.7/aa",
                                    "aaa4.2/aa",
                                    "aaa20.5/aa"
                                ],
                                "normal":[
                                    "aa/aa"
                                ],
                                "silent carrier": [
                                    "-a3.7/aa",
                                    "-a4.2/aa",
                                    "-a20.5/aa"
                                ],
                                "carrier": [
                                    "--/aaa3.7",
                                    "--/aaa4.2",
                                    "-a3.7/-a3.7",
                                    "-a4.2/-a4.2",
                                    "-a3.7/-a4.2",
                                    "--/aa",
                                    "-a20.5/-a20.5",
                                    "-a20.5/-a3.7",
                                    "-a20.5/-a4.2",
                                    "--/aaa20.5",
                                ],
                                 #Hb H disease
                                "positive for hemoglobin H disease": [
                                    "--/-a3.7",
                                    "--/-a4.2",
                                    "--/-a20.5"
                                ],
                                #Hb Bart's hydrops fetalis disease
                                "positive for hemoglobin Bart's hydrops fetalis disease": [
                                    "--/--"
                                ]                            }
                        }
                    },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "hba_carrier_4.json": {
                    "hba": {
                        "caller_name": "HBA Special Caller",
                        "Warning": {
                            "type": "genotype",
                            "phenotypeGenotypeMapping": {
                                "alpha-globin triplication":[
                                    "aaa3.7/aa",
                                    "aaa4.2/aa",
                                    "aaa20.5/aa"
                                ],
                                "normal":[
                                    "aa/aa"
                                ],
                                "silent carrier": [
                                    "-a3.7/aa",
                                    "-a4.2/aa",
                                    "-a20.5/aa"
                                ],
                                "carrier": [
                                    "--/aaa3.7",
                                    "--/aaa4.2",
                                    "-a3.7/-a3.7",
                                    "-a4.2/-a4.2",
                                    "-a3.7/-a4.2",
                                    "--/aa",
                                    "-a20.5/-a20.5",
                                    "-a20.5/-a3.7",
                                    "-a20.5/-a4.2",
                                    "--/aaa20.5",
                                ],
                                 #Hb H disease
                                "positive for hemoglobin H disease": [
                                    "--/-a3.7",
                                    "--/-a4.2",
                                    "--/-a20.5"
                                ],
                                #Hb Bart's hydrops fetalis disease
                                "positive for hemoglobin Bart's hydrops fetalis disease": [
                                    "--/--"
                                ]
                            }
                        }
                    },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "hba_silent_carrier.json": {
                    "hba": {
                        "caller_name": "HBA Special Caller",
                        "Warning": {
                            "type": "genotype",
                            "phenotypeGenotypeMapping": {
                                "alpha-globin triplication":[
                                    "aaa3.7/aa",
                                    "aaa4.2/aa",
                                    "aaa20.5/aa"
                                ],
                                "normal":[
                                    "aa/aa"
                                ],
                                "silent carrier": [
                                    "-a3.7/aa",
                                    "-a4.2/aa",
                                    "-a20.5/aa"
                                ],
                                "carrier": [
                                    "--/aaa3.7",
                                    "--/aaa4.2",
                                    "-a3.7/-a3.7",
                                    "-a4.2/-a4.2",
                                    "-a3.7/-a4.2",
                                    "--/aa",
                                    "-a20.5/-a20.5",
                                    "-a20.5/-a3.7",
                                    "-a20.5/-a4.2",
                                    "--/aaa20.5",
                                ],
                                 #Hb H disease
                                "positive for hemoglobin H disease": [
                                    "--/-a3.7",
                                    "--/-a4.2",
                                    "--/-a20.5"
                                ],
                                #Hb Bart's hydrops fetalis disease
                                "positive for hemoglobin Bart's hydrops fetalis disease": [
                                    "--/--"
                                ]
                            }
                        }
                    },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "smn_positive.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": {
                        "caller_name": "SMN Special Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "smn1CopyNumber",
                                    "operator": "EQ",
                                    "value": 0,
                                    "message": "Based on the SMN Caller, this sample is positive for Spinal Muscular Atrophy"
                                }
                            ]
                        }
                    },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "smn_carrier.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": {
                        "caller_name": "SMN Special Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "smn1CopyNumber",
                                    "operator": "EQ",
                                    "value": 1,
                                    "message": "Based on the SMN Caller, this sample is carrier for Spinal Muscular Atrophy"
                                }
                            ]
                        }
                    },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "smn_silent_carrier_risk.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": {
                        "caller_name": "SMN Special Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "smn1CopyNumber",
                                    "operator": "EQ",
                                    "value": 2,
                                    "message": "Based on the SMN Caller, this sample has increased risk of being a silent carrier (2+0) for Spinal Muscular Atrophy"
                                },
                                {
                                    "field": "variants",
                                    "operator": "CONTAINS",
                                    "value": {"alleleId": "NM_000344.4:c.*3+80T>G", "alleleCopyNumber": 1},
                                    "message": "Based on the SMN Caller, this sample has increased risk of being a silent carrier (2+0) for Spinal Muscular Atrophy"
                                }
                            ]
                        }
                    },
                    "gba": { "caller_name": "GBA Caller" },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "gba_positive_1.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": {
                        "caller_name": "GBA Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "recombinantHaplotypes",
                                    "operator": "GE",
                                    "value": 2,
                                    "message": "Based on the GBA Caller, this sample is positive for Gaucher disease"
                                }
                            ]
                        }
                    },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "gba_positive_2.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": {
                        "caller_name": "GBA Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "variants",
                                    "operator": "CONTAINS",
                                    "value": {"alleleCopyNumber": 2},
                                    "message": "Based on the GBA Caller, this sample is positive for Gaucher disease"
                                }
                            ]
                        }
                    },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "gba_multiple_phase_unknown_1.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": {
                        "caller_name": "GBA Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "recombinantHaplotypes",
                                    "operator": "EQ", 
                                    "value": 1,
                                    "message": "Multiple GBA variants detected; phase is unknown (could be in cis or in trans). Interpret cautiously."
                                },
                                {
                                    "field": "variants",
                                    "operator": "GE",
                                    "value": 1,
                                    "message": "Multiple GBA variants detected; phase is unknown (could be in cis or in trans). Interpret cautiously."
                                }
                            ]
                        }
                    },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "gba_multiple_phase_unknown_2.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": {
                        "caller_name": "GBA Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "recombinantHaplotypes",
                                    "operator": "EQ", 
                                    "value": 0,
                                    "message": "Multiple GBA variants detected; phase is unknown (could be in cis or in trans). Interpret cautiously."
                                },
                                {
                                    "field": "variants",
                                    "operator": "GE",
                                    "value": 2,
                                    "message": "Multiple GBA variants detected; phase is unknown (could be in cis or in trans). Interpret cautiously."
                                }
                            ]
                        }
                    },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "gba_carrier_1.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": {
                        "caller_name": "GBA Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "recombinantHaplotypes",
                                    "operator": "EQ", 
                                    "value": 1,
                                    "message": "Based on the GBA Caller, this sample is carrier for Gaucher disease"
                                }
                            ]
                        }
                    },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                },
                "gba_carrier_2.json": {
                    "hba": { "caller_name": "HBA Special Caller" },
                    "smn": { "caller_name": "SMN Special Caller" },
                    "gba": {
                        "caller_name": "GBA Caller",
                        "Warning": {
                            "type": "condition",
                            "conditions": [
                                {
                                    "field": "variants",
                                    "operator": "EQ", 
                                    "value": 1,
                                    "message": "Based on the GBA Caller, this sample is carrier for Gaucher disease"
                                }
                            ]
                        }
                    },
                    "lpa": {},
                    "rh": {},
                    "cyp2b6": {},
                    "cyp2d6": {},
                    "cyp21a2": {}
                }
            },
        },
        "expected": {
            "SMN1": {
                "data": {"isSMA": True, "isCarrier": True},
                "warning": "Based on SMN Special Caller, sample is POSITIVE for Spinal Muscular Atrophy"
            },
            "LPA": {
                "data": {"score": 5.5, "flag": True},
                "warning": ""
            }
        }
    }
]
@pytest.mark.parametrize("context", TEST_CONTEXTS)
def test_parser_in_memory( context : JsonDict) -> None:
    # Instantiate parser with in-memory adv_cfg
    parser = AdvancedAnalysisParser(context["request"])
    result = parser.run(return_dict=True)
    print(json.dumps(result, indent=2, default=str))
    # Compare to expected
    assert result is not None
    assert result['MSI'].get('warning') == 'MSI>10 detected in this sample'
    assert result['TMB'].get('warning') == 'TMB>10 detected in this sample'
    assert result['GIS'].get('warning') == 'GIS>42 detected in this sample'
    assert result['SMN1'].get('warning') == 'Carrier positive for Spinal Muscular Atrophy'
    assert result['GBA'].get('warning') == ''
    # Add assertions for all relevant callers in the test context
    for caller in ['hba', 'smn', 'gba', 'lpa', 'rh', 'cyp2b6', 'cyp2d6', 'cyp21a2']:
        if caller in result:
            assert 'caller_name' in result[caller]
            # Optionally check warning presence/absence
            if 'Warning' in context['request']['map_files'].get(context['request'].get('input_json', ''), {}).get(caller, {}):
                assert 'warning' in result[caller]

