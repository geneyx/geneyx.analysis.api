import os

import pytest
from AdvancedAnalysisFileParser import JsonDict
from AdvancedAnalysisFileParser import AdvancedAnalysisParser

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "Test")
TEST_CONTEXTS = [
    {
        "request": {
            "output_json": "out.json",
            "input_dir": TEST_DATA_DIR,    # path/to/input
            "input_files": [
                "test.gba.tsv",
                "test.smn.tsv",
                "test.wgs.hg38.targeted.json",
                "TruSightOncology500\\sample_ID__CombinedVariantOutput.tsv"
            ]
        }
    }
]

@pytest.mark.parametrize("context", TEST_CONTEXTS)
def test_parser_in_memory(context: JsonDict):
    parser = AdvancedAnalysisParser(context["request"])
    result = parser.run()
