import csv
import json
import logging
from dataclasses import dataclass
from typing import Dict, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@dataclass
class FieldWarning:
    threshold: float
    warning: str

@dataclass
class FieldConfig:
    # If a warning is provided, it will be used to check the field’s value.
    warning: Optional[FieldWarning] = None

@dataclass
class SectionConfig:
    # Mapping of field names to their configuration.
    include_all_fields: bool = False
    # If set to None, then all keys from the TSV are kept (and no warning checks are applied).
    fields: Optional[Dict[str, FieldConfig]] = None

class DragenTruSightOncology500TSVParser:
    def __init__(self, tsv_file_path: str):
        self.tsv_file_path = tsv_file_path

    def parse_tsv(self, sections_config: Dict[str, SectionConfig]) -> Dict[str, Any]:
        """
        Parse the TSV file while handling both key-value and table sections.

        sections_config: A dictionary where keys are section names (case-insensitive) and values are SectionConfig.
        """
        parsed_data = {}
        # Normalize section names to lowercase.
        sections_config = {k.lower(): v for k, v in sections_config.items()}

        try:
            with open(self.tsv_file_path, 'r', newline='', encoding='utf-8') as tsv_file:
                reader = csv.reader(tsv_file, delimiter='\t')
                current_section = None
                header = None  # For table sections
                key_value_section = {}  # For key-value sections
                for row in reader:
                    if not row or row[0].startswith("#"):
                        continue
                    # Remove empty cells.
                    row = [cell.strip() for cell in row if cell.strip()]
                    # Detect section headers (e.g., "[Section Name]").
                    if row and row[0].startswith('[') and row[0].endswith(']'):
                        # Process any accumulated key-value data for the previous section.
                        if key_value_section and current_section:
                            warning_text = self._apply_warnings(key_value_section, sections_config[current_section])
                            parsed_data[current_section] = {
                                "data": self._apply_filter(key_value_section, sections_config[current_section]),
                                "Warning": warning_text
                            }
                            key_value_section = {}
                        section_name = row[0].strip("[]").lower()
                        if section_name in sections_config:
                            current_section = section_name
                            parsed_data[current_section] = []  # Prepare for table rows.
                            header = None  # Reset header for the new section.
                        else:
                            current_section = None
                        continue

                    if current_section:
                        # If the row has exactly two cells, assume it's a key-value pair.
                        if len(row) == 2:
                            key, value = row
                            key_value_section[key] = value
                            continue
                        # If header is not set yet, treat the row as the table header.
                        if header is None:
                            header = row
                            continue

                        # Process table row: create a dictionary mapping header columns to row values.
                        row_data = {header[i].lower(): row[i] for i in range(min(len(header), len(row)))}
                        warning_text = self._apply_warnings(row_data, sections_config[current_section])
                        row_dict = {"data": row_data, "Warning": warning_text}
                        parsed_data[current_section].append(row_dict)

                # Process any remaining key-value section data.
                if key_value_section and current_section:
                    kv_lower = {k.lower(): v for k, v in key_value_section.items()}
                    warning_text = self._apply_warnings(kv_lower, sections_config[current_section])
                    parsed_data[current_section] = {
                        "data": self._apply_filter(kv_lower, sections_config[current_section]),
                        "Warning": warning_text
                    }
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
        except Exception as e:
            logging.error(f"An error occurred while parsing the TSV file: {e}")
        return parsed_data

    def _apply_filter(self, data: Dict[str, str], config: SectionConfig) -> Dict[str, str]:
        """
        Filter the data based on the fields provided in SectionConfig.
        If config.fields is None, return all data.
        """
        filtered = {}
        if config.include_all_fields or config.fields is None:
            for field in data.keys():
                # Use case-insensitive matching.
                if field in data:
                    filtered[field] = data[field]
            return filtered
        else:
            for field in config.fields.keys():
                # Use case-insensitive matching.
                if field in data:
                    filtered[field] = data[field]
            return filtered

    def _apply_warnings(self, data: Dict[str, str], config: SectionConfig) -> str:
        """
        Check each field defined in config.fields (if any) for warnings.
        Returns a combined warning message if any field exceeds its threshold.
        """
        if config.fields is None:
            return ""
        warnings_list = []
        for field, field_config in config.fields.items():
            if field_config.warning is not None:
                if field in data:
                    try:
                        value = float(data[field])
                        if value > field_config.warning.threshold:
                            warnings_list.append(field_config.warning.warning)
                    except ValueError:
                        pass
        return "; ".join(warnings_list)

def main():
    tsv_file_path = './sample_ID__CombinedVariantOutput.tsv'
    # Combined configuration: each field is specified once with its warning settings.
    sections_to_parse = {
        "msi": SectionConfig(
            fields={
                "Percent Unstable MSI Sites": FieldConfig(
                    warning=FieldWarning(threshold=10, warning="MSI>10 detected in this sample")
                )
            }
        ),
        "tmb": SectionConfig(
            fields={
                "Total TMB": FieldConfig(
                    warning=FieldWarning(threshold=10, warning="TMB>10 detected in this sample")
                )
            }
        ),
        "gis": SectionConfig(
            include_all_fields=True,
            fields={
                "Genomic Instability Score": FieldConfig(
                    warning=FieldWarning(threshold=42, warning="GIS>42 detected in this sample")
                )
            }
        )
    }

    parser = DragenTruSightOncology500TSVParser(tsv_file_path)
    parsed_data = parser.parse_tsv(sections_to_parse)
    print(json.dumps(parsed_data, indent=4))

if __name__ == "__main__":
    main()
