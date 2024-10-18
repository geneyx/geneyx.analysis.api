#!/usr/bin/env python3
import argparse

from UnifyVcf import run

def add_chr_prefix_to_variants(file_path):
    """
    Add 'chr' to variants in the VCF file that lack it.
    """
    if not file_path:
        return None
    
    updated_lines = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Skip header lines
            if line.startswith('#'):
                updated_lines.append(line)
                continue
            
            # Split VCF columns (chromosome is in the first column)
            columns = line.split('\t')
            if not columns[0].startswith('chr'):
                columns[0] = 'chr' + columns[0]
            
            # Reconstruct the line
            updated_lines.append('\t'.join(columns))
    
    # Write the updated file
    with open(file_path, 'w') as file:
        for line in updated_lines:
            file.write(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter PacBio repeats file with pre-defined bed file and unify structural VCF files')
    parser.add_argument('-o', '--outputPath', help='The unified output VCF path (required)', required=True)
    parser.add_argument('-s', '--svPath', help='SV input file path (optional)', required=False, default=None)
    parser.add_argument('-c', '--cnvPath', help='CNV input file path (optional)', required=False, default=None)
    parser.add_argument('-r', '--repeatPath', help='Repeats input file path (optional)', required=False, default=None)

    args = parser.parse_args()

    # Process files to add 'chr' prefix if missing
    add_chr_prefix_to_variants(args.svPath)
    add_chr_prefix_to_variants(args.cnvPath)
    add_chr_prefix_to_variants(args.repeatPath)

    # A flag indicating whether to add the SVTYPE=REP to the repeats lines or not
    skip_svtype = True
    run(args.outputPath, args.svPath, args.cnvPath, args.repeatPath, skip_svtype)
