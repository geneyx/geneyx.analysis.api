#!/usr/bin/env python3
import argparse
import json
import logging
import os
import re
from typing import Optional
from pathlib import Path
from .Models import *
from .Warnings import *
from .Parsers import *
from .AdvancedAnalysisConstants import AdvancedAnalysisConstants

class AdvancedAnalysisParser:
    """
    Parse special callers outputs into unified JSON format.
    The input files are specified in a configuration JSON file.
    The output is a JSON file with the parsed data and warnings.
    """
    def __init__(self, json_request: JsonDict) -> None:
        self.config: JsonDict = json_request
        self.sequance: str = json_request.get(AdvancedAnalysisConstants.SEQUENCE_ID, '')
        self.output_dir: str = self.config.get(AdvancedAnalysisConstants.OUTPUT_DIR, '.')
        self.input_dir: str = self.config.get(AdvancedAnalysisConstants.INPUT_DIR, '.')
        self.output_json: str = self.config.get(AdvancedAnalysisConstants.OUTPUT_JSON, 'adv_analysis_output.json')
        self.map_files: JsonDict = self.config.get(AdvancedAnalysisConstants.MAP_FILES, {})
        if not self.map_files or self.map_files == {}:
            raise ValueError(f"Config must include {AdvancedAnalysisConstants.MAP_FILES}")
    
    def run(self, return_dict: bool = False) -> Optional[JsonDict]:
        logging.info("Started parsing Advanced Analysis files")
        result: JsonDict = {}
        for filename in self.map_files.keys():
            parser: IAdvancedAnalysisFileParser = AdvancedAnalysisFileParserFactory.get_parser(self.config,filename)
            callers = self.map_files[filename]
            for caller_name, caller_config in callers.items():
                caller_data: JsonDict = parser.parse( {caller_name: caller_config})
                caller_title = caller_config.get("caller_name", None)
                fields = caller_config.get("fields", None)
                fields = {k: v for k, v in fields.items()} if isinstance(fields, dict) else fields
                if fields is None:
                    caller_warning = caller_config.get(AdvancedAnalysisConstants.WARNING_KEY, None)
                    if caller_warning:
                        warning_formatter: IWarning = WarningFactory.get_formatter(caller_warning)
                        warning_text = warning_formatter.format(caller_warning, caller_data)
                        if result.get(caller_name.upper()) is None:
                            result[caller_name.upper()] = {"data": {}, "warning": {}}
                        result[caller_name.upper()]["caller_name"] = caller_title
                        result[caller_name.upper()]["data"] = caller_data
                        result[caller_name.upper()]["warning"] = warning_text
                    else:
                        if result.get(caller_name.upper()) is None:
                            result[caller_name.upper()] = {"data": {}}
                        result[caller_name.upper()]["caller_name"] = caller_title
                        result[caller_name.upper()] = {"data": caller_data}
                else:
                    for field in fields:
                        field_config = fields.get(field, {})
                        caller_warning = field_config.get(AdvancedAnalysisConstants.WARNING_KEY, None)
                        if caller_warning:
                            for cond_dict in caller_warning.get("conditions", []):
                                cond_dict["field"] = field
                            warning_formatter: IWarning = WarningFactory.get_formatter(caller_warning)
                            warning_text = warning_formatter.format(caller_warning, caller_data[caller_name][field])
                            if result.get(caller_name.upper()) is None:
                                result[caller_name.upper()] = {"data": {}, "warning": {}}
                            result[caller_name.upper()]["caller_name"] = caller_title
                            result[caller_name.upper()]["warning"] = warning_text
                            result[caller_name.upper()]["data"][field] = caller_data[caller_name][field]
                        else:
                            if result.get(caller_name.upper()) is None:
                                result[caller_name.upper()] = {"data": {}}
                            result[caller_name.upper()]["caller_name"] = caller_title
                            result[caller_name.upper()]["data"][field] = caller_data[caller_name][field]
        if return_dict:
            return result
        out_path = os.path.join(self.output_dir, self.output_json)
        with open(out_path, 'w') as f:
            json.dump(result, f, indent=4)
        logging.info(f"Wrote unified JSON to {out_path}")
        return None

    @staticmethod
    def _threshold_warning(w: JsonDict, parsed: JsonDict, value_key: str, threshold_key: str, label: str) -> str:
        name = w.get("caller_name")
        key = w.get(value_key)
        threshold = w.get(threshold_key)
        val = parsed.get(key or "")
        if isinstance(val, (int, float)) and threshold is not None and val >= threshold:
            return f"Based on {name}, sample {label} {val} ≥ {threshold}"
        return ""

    @staticmethod
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Parse special callers outputs into unified JSON"
        )
        parser.add_argument(
            "-c", "--config", required=True,
            help="Path to config JSON file"
        )
        return parser.parse_args()

    @classmethod
    def from_cli(cls) -> None:
        args = cls.parse_args()
        parser = cls(args.config)
        parser.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    AdvancedAnalysisParser.from_cli()
