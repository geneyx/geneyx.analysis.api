#!/usr/bin/env python3
"""Unify Oxford Nanopore structural VCF files into one VCF for Geneyx.

Takes the separate files an ONT pipeline produces and writes the single sorted, bgzipped
VCF that Geneyx accepts as an SV VCF, rewriting the records that need it on the way.

Usage:

    # SV and CNV
    python3 ONTUnifyVcf.py -o unified.vcf -s sv.vcf.gz -c cnv.vcf.gz

    # with repeats called by STRaglr, which need -modify to be read as repeats
    python3 ONTUnifyVcf.py -o unified.vcf -s sv.vcf.gz -r repeats.vcf.gz -modify

Run with --help for the full list of arguments, and see README.md for what each one
means and which are specific to Oxford Nanopore.

The implementation is the UnifyVcf package, which the Geneyx pipeline uses too, so a
file unified here matches what Geneyx produces internally:

    pip install UnifyVcf

Installing it also puts `ont-unify-vcf` on PATH, which takes the same arguments and is
the preferred way to run this. This file stays so the older
`python3 ONTUnifyVcf.py ...` invocation keeps working.
"""

from UnifyVcf import ont_from_cli

if __name__ == '__main__':
    ont_from_cli()
