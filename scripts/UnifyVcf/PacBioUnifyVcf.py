#!/usr/bin/env python3
"""Unify PacBio structural VCF files into one VCF for Geneyx.

Takes the separate files a PacBio pipeline produces and writes the single sorted, bgzipped
VCF that Geneyx accepts as an SV VCF, rewriting the records that need it on the way.

Usage:

    # SV only
    python3 PacBioUnifyVcf.py -o unified.vcf -s sv.vcf.gz

    # with TRGT repeats, restricted to the pathogenic-STR catalog shipped here.
    # Without -b the repeats are left out of the unified file entirely.
    python3 PacBioUnifyVcf.py -o unified.vcf -s sv.vcf.gz \
        -r sample.GRCh38.trgt.sorted.vcf.gz \
        -b STRchive-disease-loci.hg38.TRGT.bed

Run with --help for the full list of arguments, and see README.md for what each one
means and which are specific to PacBio.

The implementation is the UnifyVcf package, which the Geneyx pipeline uses too, so a
file unified here matches what Geneyx produces internally:

    pip install UnifyVcf

Installing it also puts `pacbio-unify-vcf` on PATH, which takes the same arguments and is
the preferred way to run this. This file stays so the older
`python3 PacBioUnifyVcf.py ...` invocation keeps working.
"""

from UnifyVcf import pacbio_from_cli

if __name__ == '__main__':
    pacbio_from_cli()
