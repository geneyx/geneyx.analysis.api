#!/usr/bin/env python3

import gzip
import sys

REMOVE_ALTS = {"<REF>", "<NON_REF>"}

# FORMAT fields that usually contain REF + ALT values
NUMBER_R_FORMATS = {"AD", "F1R2", "F2R1"}

# FORMAT fields that usually contain ALT-only values
NUMBER_A_FORMATS = {"AF"}


def open_text(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")


def gt_uses_removed_allele(gt, removed_indexes):
    if gt in {".", "./.", ".|."}:
        return False

    alleles = gt.replace("|", "/").split("/")
    for allele in alleles:
        if allele == ".":
            continue
        if int(allele) in removed_indexes:
            return True

    return False


def reindex_gt(gt, allele_map):
    sep = "|" if "|" in gt else "/"
    alleles = gt.replace("|", "/").split("/")
    new_alleles = []

    for allele in alleles:
        if allele == ".":
            new_alleles.append(".")
        else:
            new_alleles.append(str(allele_map[int(allele)]))

    return sep.join(new_alleles)


def subset_number_r(value, kept_indexes):
    values = value.split(",")
    return ",".join(values[i] for i in kept_indexes if i < len(values))


def subset_number_a(value, kept_alt_indexes):
    values = value.split(",")
    return ",".join(values[i - 1] for i in kept_alt_indexes if i - 1 < len(values))


def log_invalid(invalid_out, invalid_log, original_line, chrom, pos, reason):
    invalid_out.write(original_line + "\n")
    invalid_log.write(f"{chrom}:{pos}\t{reason}\n")


def process_vcf(input_vcf, output_vcf):
    invalid_vcf = output_vcf + ".invalid.vcf"
    invalid_log = output_vcf + ".invalid.log"

    total = kept = removed_symbolic = skipped = 0

    with open_text(input_vcf) as inp, \
         open(output_vcf, "w") as out, \
         open(invalid_vcf, "w") as invalid_out, \
         open(invalid_log, "w") as invalid_reason:

        for line in inp:
            line = line.rstrip("\n")

            if line.startswith("#"):
                out.write(line + "\n")
                invalid_out.write(line + "\n")
                continue

            total += 1
            original_line = line
            fields = line.split("\t")

            if len(fields) < 8:
                skipped += 1
                log_invalid(
                    invalid_out,
                    invalid_reason,
                    original_line,
                    "UNKNOWN",
                    "UNKNOWN",
                    "Malformed VCF line: fewer than 8 columns"
                )
                continue

            chrom = fields[0]
            pos = fields[1]
            alts = fields[4].split(",")

            kept_alt_indexes = []
            removed_alt_indexes = []

            for i, alt in enumerate(alts, start=1):
                if alt in REMOVE_ALTS:
                    removed_alt_indexes.append(i)
                else:
                    kept_alt_indexes.append(i)

            # No symbolic alleles to remove
            if not removed_alt_indexes:
                out.write(original_line + "\n")
                kept += 1
                continue

            removed_symbolic += 1

            # If all ALTs were <REF>/<NON_REF>, drop the record
            if not kept_alt_indexes:
                skipped += 1
                log_invalid(
                    invalid_out,
                    invalid_reason,
                    original_line,
                    chrom,
                    pos,
                    "All ALT alleles were <REF>/<NON_REF>"
                )
                continue

            # Build allele map: REF stays 0; kept ALT indexes are re-numbered
            allele_map = {0: 0}
            for new_idx, old_idx in enumerate(kept_alt_indexes, start=1):
                allele_map[old_idx] = new_idx

            reject_reason = None

            # FORMAT/sample handling
            if len(fields) >= 10:
                format_keys = fields[8].split(":")

                for sample_col in range(9, len(fields)):
                    sample_values = fields[sample_col].split(":")

                    if len(sample_values) != len(format_keys):
                        reject_reason = (
                            f"FORMAT/sample value count mismatch in sample column {sample_col + 1}"
                        )
                        break

                    fmt = dict(zip(format_keys, sample_values))

                    # Drop if GT references a removed allele
                    if "GT" in fmt:
                        try:
                            if gt_uses_removed_allele(fmt["GT"], set(removed_alt_indexes)):
                                reject_reason = (
                                    f"GT {fmt['GT']} references removed ALT allele "
                                    f"{removed_alt_indexes}"
                                )
                                break
                        except ValueError:
                            reject_reason = f"Invalid GT value: {fmt['GT']}"
                            break

                        try:
                            fmt["GT"] = reindex_gt(fmt["GT"], allele_map)
                        except KeyError:
                            reject_reason = f"GT {fmt['GT']} references missing ALT allele after reindexing"
                            break

                    # REF + ALT fields
                    kept_r_indexes = [0] + kept_alt_indexes
                    for key in NUMBER_R_FORMATS:
                        if key in fmt and fmt[key] not in {".", ""}:
                            fmt[key] = subset_number_r(fmt[key], kept_r_indexes)

                    # ALT-only fields
                    for key in NUMBER_A_FORMATS:
                        if key in fmt and fmt[key] not in {".", ""}:
                            fmt[key] = subset_number_a(fmt[key], kept_alt_indexes)

                    fields[sample_col] = ":".join(fmt[k] for k in format_keys)

            if reject_reason:
                skipped += 1
                log_invalid(
                    invalid_out,
                    invalid_reason,
                    original_line,
                    chrom,
                    pos,
                    reject_reason
                )
                continue

            # Update ALT field
            fields[4] = ",".join(alts[i - 1] for i in kept_alt_indexes)

            out.write("\t".join(fields) + "\n")
            kept += 1

    print("Processing complete.")
    print(f"Input records: {total}")
    print(f"Records written: {kept}")
    print(f"Records with symbolic ALT removed: {removed_symbolic}")
    print(f"Records skipped as invalid: {skipped}")
    print(f"Clean VCF: {output_vcf}")
    print(f"Invalid VCF: {invalid_vcf}")
    print(f"Invalid log: {invalid_log}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: clean_nonref_vcf.py input.vcf[.gz] output.vcf")
        sys.exit(1)

    process_vcf(sys.argv[1], sys.argv[2])