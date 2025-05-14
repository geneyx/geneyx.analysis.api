import csv
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from .IAdvancedAnalysisFileParser import IAdvancedAnalysisFileParser
from ..Models import JsonDict, SectionConfig


class DragenTruSightOncology500TSVParser(IAdvancedAnalysisFileParser):
    """
    Parser for CombinedVariantOutput TSV.
    Reads only configured sections and fields, streaming parse inside loader.
    """
    def parse(self, config: JsonDict) -> JsonDict:
        """
        Entry point: prepare section configs and delegate to loader-parsing function.
        """
        sections = self._prepare_configs(config)
        return self._load_and_parse_sections(sections)

    def _load_and_parse_sections(
        self,
        sections: Dict[str, Union[SectionConfig, dict]]
    ) -> JsonDict:
        """
        Open TSV, detect requested sections, parse key/value and table rows
        on the fly according to each section's fields or include_all flag.
        Returns a JsonDict mapping section names to extracted data.
        """
        result: JsonDict = {}
        headers: Dict[str, List[str]] = {}

        # Track for each section its cfg, fields, include_all, and accumulated list
        state: Dict[str, Tuple[JsonDict, bool]] = {}

        current_section: Optional[str] = None
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            for raw in reader:
                if not raw or raw[0].startswith('#'):
                    continue
                row = [c.strip() for c in raw if c.strip()]
                if not row:
                    continue
                # Section header
                if row[0].startswith('[') and row[0].endswith(']'):
                    sec = row[0].strip('[]')
                    if sec in sections:
                        current_section = sec
                        cfg = sections[sec]
                        fields, include_all = self._extract_fields(cfg)
                        state[sec] = (fields, include_all)
                        result[sec] = {}
                        headers.pop(sec, None)
                    else:
                        current_section = None
                    continue

                if current_section is None:
                    continue

                fields, include_all = state[current_section]
                # Before header: KV pairs or header row
                if current_section not in headers:
                    # KV pair
                    if len(row) == 2:
                        key, val = row
                        key_l = key
                        if include_all or key_l in fields:
                            result[current_section][key_l] = IAdvancedAnalysisFileParser._format_value(val)
                        continue
                    # Header row
                    hdr = [h for h in row]
                    if not include_all and fields:
                        allowed = set(f for f in fields)
                        hdr = [h for h in hdr if h in allowed]
                    headers[current_section] = hdr
                    continue

                # Table row
                hdr = headers[current_section]
                for i in range(min(len(hdr), len(row))):
                    result[current_section].append(IAdvancedAnalysisFileParser._format_value(row[i]))

        # Post-process: unwrap single KV-only sections
        for sec, entries in list(result.items()):
            hdr = headers.get(sec)
            if hdr is None and len(entries) == 1:
                result[sec] = entries
        return result

    def _prepare_configs(self, config: JsonDict) -> Dict[str, Union[SectionConfig, dict]]:
        return {k: v for k, v in config.items()}

    def _extract_fields(
        self,
        cfg: Union[SectionConfig, dict]
    ) -> Tuple[JsonDict, bool]:
        if isinstance(cfg, SectionConfig):
            return cfg.fields or {}, cfg.include_all_fields
        raw_fields = cfg.get('fields') or {}
        include_all = cfg.get('include_all_fields', False)
        raw_fields = {k: v for k, v in raw_fields.items()}
        if isinstance(raw_fields, dict):
            raw_fields = {k: None for k in raw_fields}
        return raw_fields, include_all