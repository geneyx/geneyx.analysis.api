#!/usr/bin/env python3
import os
import logging
import argparse

from UnifyVcf import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter PacBio repeats file with pre-defined bed file and unify structural vcf files')
    parser.add_argument('-o', '--outputPath', help='the unified output VCF path (required)', required=True)
    parser.add_argument('-s', '--svPath', help='SV input file path (optional)', required=False, default=None)
    parser.add_argument('-c', '--cnvPath', help='CNV input file path (optional)', required=False, default=None)
    parser.add_argument('-r', '--repeatPath', help='repeats input file path (optional)', required=False, default=None)


    args = parser.parse_args()
    # a flag indicating whether to add the SVTYPE=REP to the repeats lines or not
    skip_svtype = True
    run(args.outputPath, args.svPath, args.cnvPath, args.repeatPath, skip_svtype)
