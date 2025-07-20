from .IWarning import IWarning
from ..Models import JsonDict
class GenotypeWarning(IWarning):
    def format(self, config: JsonDict, data: JsonDict) -> str:
        name = config.get("caller_name") or config.get("name")
        sample = data.get("genotype")
        mapping = config.get("phenotypeGenotypeMapping") or config.get("phenotype_genotype_mapping") or {}
        warning = ""
        if sample in mapping:
            warning = f"Based on {name}, this sample is defined as <b>{mapping[sample]}</b>"
        return warning