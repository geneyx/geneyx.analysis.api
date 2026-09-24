#!/usr/bin/env python3
"""Add a 'chr' prefix to ONT structural calls, then unify them into one VCF.

The input files are rewritten in place, so a failed run leaves them prefixed.
Re-running is safe: a record whose chromosome already starts with 'chr' is left
alone.

Usage:

    python3 ONT_AppendChr.py -o unified.vcf -s sv.vcf -c cnv.vcf -r repeats.vcf

The unification is the UnifyVcf package, which the Geneyx pipeline uses too:

    pip install UnifyVcf
"""

import argparse

from UnifyVcf import run


def add_chr_prefix_to_variants(file_path):
    """
    Add 'chr' to variants in the VCF file that lack it.
    """
    if not file_path:
        return None

    updated_lines = []

    with open(file_path, "r") as file:
        for line in file:
            # Skip header lines
            if line.startswith("#"):
                updated_lines.append(line)
                continue

            # Split VCF columns (chromosome is in the first column)
            columns = line.split("\t")
            if not columns[0].startswith("chr"):
                columns[0] = "chr" + columns[0]

            # Reconstruct the line
            updated_lines.append("\t".join(columns))

    # Write the updated file
    with open(file_path, "w") as file:
        for line in updated_lines:
            file.write(line)


def main(argv=None):
    """Prefix the inputs and unify them; returns the unified .gz path."""
    parser = argparse.ArgumentParser(
        description="Add a chr prefix to ONT structural calls and unify them into one VCF"
    )
    parser.add_argument(
        "-o",
        "--outputPath",
        help="The unified output VCF path (required)",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--svPath",
        help="SV input file path (optional)",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-c",
        "--cnvPath",
        help="CNV input file path (optional)",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-r",
        "--repeatPath",
        help="Repeats input file path (optional)",
        required=False,
        default=None,
    )

    args = parser.parse_args(argv)

    # Process files to add 'chr' prefix if missing
    add_chr_prefix_to_variants(args.svPath)
    add_chr_prefix_to_variants(args.cnvPath)
    add_chr_prefix_to_variants(args.repeatPath)

    # Every argument by keyword. This call used to pass a skip-SVTYPE flag
    # positionally, where it landed in roh_bed_path instead: the flag never applied,
    # and the unifier went on to read True as an ROH file - which opens file
    # descriptor 1 and closes the process's own stdout on the way out.
    #
    # There is no flag now. UnifyVcf decides per record whether a repeat call needs
    # ;SVTYPE=REP and appends it only where the record carries no SVTYPE of its own,
    # so ONT calls that already carry SVTYPE=STR are left alone - which is what the
    # flag was for - and STRaglr calls that carry none are marked, without which
    # Geneyx does not read them as repeats at all.
    return run(
        output_path=args.outputPath,
        sv_path=args.svPath,
        cnv_path=args.cnvPath,
        repeat_path=args.repeatPath,
    )


if __name__ == "__main__":
    main()
