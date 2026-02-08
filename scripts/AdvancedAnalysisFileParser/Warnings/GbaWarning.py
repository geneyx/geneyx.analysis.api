from .IWarning import IWarning
from ..Models import JsonDict

class GbaWarning(IWarning):
    def format(self, config: JsonDict, data: JsonDict) -> str:
        name = config.get("caller_name") or config.get("name") or "GBA Caller"
        disease = config.get("disease_name") or config.get("disease") or "Gaucher disease"

        rec_list = [x for x in (data.get("recombinantHaplotypes") or []) if x]
        rec_count = len(rec_list)

        nonrec = []
        for v in data.get("variants", []) or []:
            # treat strings as nonrecombinant variants without copy number (defaults to 1 for counting phase-unknown conditions)
            if isinstance(v, dict) or isinstance(v, str):
                nonrec.append(v)

        # Helper counts
        def allele_copy(v):
            if isinstance(v, dict):
                ac = (
                    v.get("alleleCopyNumber")
                    or v.get("allele_copy_number")
                    or v.get("altCopyNumber")
                )
                return ac if isinstance(ac, (int, float)) else 0
            # if variant represented as string, assume copy number 1 for phase-unknown heuristics
            if isinstance(v, str):
                return 1
            return 0

        any_nonrec_ge2 = any(allele_copy(v) >= 2 for v in nonrec)
        nonrec_eq1 = [v for v in nonrec if allele_copy(v) == 1]
        nonrec_eq1_count = len(nonrec_eq1)

        # Positive: evidence of two affected alleles
        if rec_count >= 2 or any_nonrec_ge2:
            return f"Based on the {name}, this sample is positive for {disease}"

        # Phase unknown: mixed findings
        if (rec_count == 1 and nonrec_eq1_count >= 1) or (rec_count == 0 and nonrec_eq1_count >= 2):
            return (
                "Multiple GBA variants detected; phase is unknown (could be in cis or in trans). Interpret cautiously."
            )

        # Carrier: exactly one affected allele
        if (rec_count == 1 and nonrec_eq1_count == 0 and not any_nonrec_ge2) or (rec_count == 0 and nonrec_eq1_count == 1):
            return f"Based on the {name}, this sample is carrier for {disease}"

        return ""
