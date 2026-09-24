#!/usr/bin/env python3
"""Unify DRAGEN structural VCF files into one VCF for Geneyx.

Takes the separate files DRAGEN produces and writes the single sorted, bgzipped
VCF that Geneyx accepts as an SV VCF, rewriting the records that need it on the way.

Usage:

    # SV and CNV
    python3 DragenUnifyVcf.py -o unified.vcf -s sv.vcf.gz -c cnv.vcf.gz

    # adding repeats, and the ROH bed DRAGEN writes under --vc-enable-roh
    python3 DragenUnifyVcf.py -o unified.vcf -s sv.vcf.gz -c cnv.vcf.gz \
        -r repeats.vcf.gz -d sample.roh.bed

Run with --help for the full list of arguments, and see README.md for what each one
means and which are specific to DRAGEN.

The implementation is the UnifyVcf package, which the Geneyx pipeline uses too, so a
file unified here matches what Geneyx produces internally:

    pip install UnifyVcf

Installing it also puts `dragen-unify-vcf` on PATH, which takes the same arguments and is
the preferred way to run this. This file stays so the older
`python3 DragenUnifyVcf.py ...` invocation keeps working.
"""

from UnifyVcf import dragen_from_cli

if __name__ == '__main__':
    dragen_from_cli()
