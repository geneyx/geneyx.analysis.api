#!/usr/bin/env python3

import gzip
import sys


def open_text(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")


def is_hom_ref_or_missing(gt):
    """
    Returns True if GT is:
    - homozygous reference: 0/0, 0|0, 0
    - missing: ./., .|., .
    """
    if gt in {".", "./.", ".|.", ""}:
        return True

    alleles = gt.replace("|", "/").split("/")
    return all(a == "0" for a in alleles)


def get_gt_from_sample(format_keys, sample_value):
    if "GT" not in format_keys:
        return None

    gt_index = format_keys.index("GT")
    sample_values = sample_value.split(":")

    if len(sample_values) <= gt_index:
        return None

    return sample_values[gt_index]


def should_drop_all_hom_ref_or_missing(fields):
    """
    Drop only if all samples with GT are homozygous reference or missing.
    Keep if any sample has a non-reference GT.
    """
    if len(fields) < 10:
        return False

    format_keys = fields[8].split(":")

    if "GT" not in format_keys:
        return False

    found_gt = False

    for sample_col in range(9, len(fields)):
        gt = get_gt_from_sample(format_keys, fields[sample_col])

        if gt is None:
            continue

        found_gt = True

        if not is_hom_ref_or_missing(gt):
            return False

    return found_gt


def process_vcf(input_vcf, output_vcf):
    total = 0
    written = 0
    dropped_hom_ref_or_missing = 0
    rewritten_records = 0
    rewritten_alleles = 0

    with open_text(input_vcf) as inp, open(output_vcf, "w") as out:
        for line in inp:
            line = line.rstrip("\n")

            if line.startswith("#"):
                out.write(line + "\n")
                continue

            total += 1
            fields = line.split("\t")

            if len(fields) < 8:
                out.write(line + "\n")
                written += 1
                continue

            if should_drop_all_hom_ref_or_missing(fields):
                dropped_hom_ref_or_missing += 1
                continue

            alts = fields[4].split(",")

            new_alts = []
            changed = False

            for alt in alts:
                if alt == "<NON_REF>":
                    new_alts.append("<REF>")
                    rewritten_alleles += 1
                    changed = True
                else:
                    new_alts.append(alt)

            if changed:
                rewritten_records += 1

            fields[4] = ",".join(new_alts)

            out.write("\t".join(fields) + "\n")
            written += 1

    print("Processing complete.")
    print(f"Input records: {total}")
    print(f"Records written: {written}")
    print(f"Records dropped because all GTs were 0/0, 0|0, ./., .|., or .: {dropped_hom_ref_or_missing}")
    print(f"Records with <NON_REF> rewritten: {rewritten_records}")
    print(f"<NON_REF> alleles rewritten to <REF>: {rewritten_alleles}")
    print(f"Clean VCF: {output_vcf}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: clean_nonref_vcf.py input.vcf[.gz] output.vcf")
        sys.exit(1)

    process_vcf(sys.argv[1], sys.argv[2])
