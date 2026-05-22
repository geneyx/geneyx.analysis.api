#!/usr/bin/env python3

import gzip
import sys


def open_text(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")


def process_vcf(input_vcf, output_vcf):
    total = 0
    written = 0
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
                # Write malformed/nonstandard lines unchanged
                out.write(line + "\n")
                written += 1
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

            # Important:
            # Do NOT modify GT, AD, AF, or any FORMAT fields.
            # Allele indexes stay exactly the same.
            out.write("\t".join(fields) + "\n")
            written += 1

    print("Processing complete.")
    print(f"Input records: {total}")
    print(f"Records written: {written}")
    print(f"Records with <NON_REF> rewritten: {rewritten_records}")
    print(f"<NON_REF> alleles rewritten to <REF>: {rewritten_alleles}")
    print(f"Clean VCF: {output_vcf}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: clean_nonref_vcf.py input.vcf[.gz] output.vcf")
        sys.exit(1)

    process_vcf(sys.argv[1], sys.argv[2])