from .IWarning import IWarning
from ..Models import JsonDict

class SmnWarning(IWarning):
    def format(self, config: JsonDict, data: JsonDict) -> str:
        name = config.get("caller_name") or config.get("name") or "SMN Caller"
        disease = config.get("disease_name") or config.get("disease") or "Spinal Muscular Atrophy"
        smn1_cn = data.get("smn1CopyNumber")
        # Positive if smn1CopyNumber == 0
        if isinstance(smn1_cn, (int, float)) and smn1_cn == 0:
            return f"Based on the {name}, this sample is positive for {disease}"
        # Carrier if smn1CopyNumber == 1
        if isinstance(smn1_cn, (int, float)) and smn1_cn == 1:
            return f"Based on the {name}, this sample is carrier for {disease}"
        # Silent carrier risk if smn1CopyNumber == 2 and specific variant has alleleCopyNumber >= threshold
        if isinstance(smn1_cn, (int, float)) and smn1_cn == 2:
            for v in data.get("variants", []) or []:
                # variants may be strings or dicts with keys like 'alleleId', 'hgvs', 'name', 'variantName', 'id'
                if isinstance(v, str):
                    vid = v
                    ac = 1  # presence implies >=1 when encoded as string only
                elif isinstance(v, dict):
                    vid = v.get("alleleId") or v.get("hgvs") or v.get("name") or v.get("variantName") or v.get("id") or ""
                    ac = (v.get("alleleCopyNumber") or v.get("allele_copy_number") or v.get("altCopyNumber"))
                else:
                    continue
                if vid != "" and isinstance(ac, (int, float)) and ac >= 1:
                    return (f"Based on the {name}, this sample has increased risk of being a silent carrier {vid} for {disease}")
        return ""
