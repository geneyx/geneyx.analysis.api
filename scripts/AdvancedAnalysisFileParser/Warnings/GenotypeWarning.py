from .IWarning import IWarning
from ..Models import JsonDict
class GenotypeWarning(IWarning):
    def format(self, config: JsonDict, data: JsonDict) -> str:
        name = config.get("caller_name") or config.get("name")
        genotype_key = config.get("genotype_data_key", "genotype")
        sample = data.get(genotype_key)
        mapping = config.get("phenotypeGenotypeMapping") or config.get("phenotype_genotype_mapping") or {}
        warning = ""
        found_phenotype = None
        for phenotype, genotypes in mapping.items():
            if sample in genotypes:
                found_phenotype = phenotype
                break
        if found_phenotype:
            warning = f"Based on {name}, this sample is defined as <b>{found_phenotype}</b>"
        return warning
