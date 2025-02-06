#!/usr/bin/env python3
import os
import logging
import argparse
import subprocess

from UnifyVcf import run

def filter_repeats_vcf(full_repeat_path: str = None, repeat_bed_file_path: str = None)->str:
    
    # returns None if the pathes received are None  
    if full_repeat_path is None or repeat_bed_file_path is None:
        if(full_repeat_path is None):
            logging.warning(f'Can\'t filter repeats file "{full_repeat_path}". The file does not exist')
        elif(repeat_bed_file_path is None):
            logging.warning(f'Can\'t filter repeats file with "{repeat_bed_file_path}". The bed file does not exist')
        return None
    
    if(not os.path.exists(full_repeat_path)):
        logging.warning(f'{full_repeat_path} file doesn\'t exist')
        return None
    if(not os.path.exists(repeat_bed_file_path)):
        logging.warning(f'{repeat_bed_file_path} doesn\'t exist')
        return None
        
    repeat_file_name = os.path.basename(full_repeat_path)
    repeat_file_directory = os.path.dirname(full_repeat_path)
    repeat_suffix = ''
    while(repeat_suffix != '.vcf'):
        (repeat_file, repeat_suffix) = os.path.splitext(repeat_file_name)
        repeat_file_name = repeat_file

    filtered_repeat_path = os.path.join(repeat_file_directory, repeat_file_name + '_filtered.vcf')
    filtering_command = f'bedtools intersect -a {full_repeat_path} -b {repeat_bed_file_path} -header > {filtered_repeat_path}'
    subprocess.run(filtering_command,
                   shell=True, 
                   executable='/bin/bash', 
                   check=True)
    
    return filtered_repeat_path
    

def filter_and_run(output_path: str, sv_path: str = None, cnv_path: str = None, full_repeat_path: str = None, repeat_bed_file_path: str = None):
    
    # perform the filtering here and save the new repeats file into the same directory the full repeats are taken from
    # but with an informative suffix
    filtered_repeat_path = filter_repeats_vcf(full_repeat_path, repeat_bed_file_path)
    
    # a flag indicating whether to add the SVTYPE=REP to the repeats lines or not
    skip_svtype = False
    
    run(output_path=output_path, sv_path=sv_path, cnv_path=cnv_path, repeat_path=filtered_repeat_path, skip_svtype=skip_svtype)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter PacBio repeats file with pre-defined bed file and unify structural vcf files')
    parser.add_argument('-o', '--outputPath', help='the unified output VCF path (required)', required=True)
    parser.add_argument('-s', '--svPath', help='SV input file path (optional)', required=False, default=None)
    parser.add_argument('-c', '--cnvPath', help='CNV input file path (optional)', required=False, default=None)
    parser.add_argument('-r', '--fullRepeatPath', help='Full repeats input file path (optional)', required=False, default=None)
    parser.add_argument('-b', '--repeatLocationsBedFilePath', help='Repeats filtering bed file path (optional)', required=False, default=None)

    args = parser.parse_args()
    filter_and_run(args.outputPath, args.svPath, args.cnvPath, args.fullRepeatPath, args.repeatLocationsBedFilePath)
