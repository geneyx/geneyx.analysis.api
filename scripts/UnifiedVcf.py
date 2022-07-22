#!/usr/bin/env python3
import gzip
import os
import logging
import argparse


def __get_lines__(file_path: str) -> []:
    """ Gets a file and return its lines.
    This is done in order to handle both zipped and unzipped files.
    """
    try:
        with gzip.open(file_path, 'rt') as file_h:
            lines = file_h.readlines()
    except:
        with open(file_path) as file_h:
            lines = file_h.readlines()
    return lines


def __modify_repeat_line__(repeat_line: str) -> str:
    (chrom, pos, id, ref, alt, qual, filter, info, format, _) = repeat_line.split("\t")
    info = info + ';SVTYPE=REP'
    repeat_line = "\t".join((chrom, pos, id, ref, alt, qual, filter, info, format, _))
    return repeat_line


def __is_valid_line__(line: str) -> bool:
    # check if line is header or null / empty
    if line.startswith('#') or not line:
        return True

    cells = line.split('\t')
    info_cell = cells[7]
    format_key = cells[8]
    format_value = cells[9]

    # if the "svtype" line is exists the line valid
    if 'SVTYPE=' in info_cell:
        return True

    gt_index = format_key.split(':').index('GT')
    gt_value = format_value.split(':')[gt_index]

    # if "svtype" not present and GT is 0 or "./." the line is invalid
    if gt_index == '0' or gt_value == './.':
        return False

    return True


def __write_vcf_content__(ftype: str, lines_dict: dict, output_h):
    start_read_content_flag = False
    for vcf_line in lines_dict[ftype]:
        if start_read_content_flag:
            if ftype == 'repeat':
                vcf_line = __modify_repeat_line__(vcf_line)
            output_h.write(vcf_line)
        if vcf_line.find('#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT') != -1:
            start_read_content_flag = True

    if not start_read_content_flag:
        logging.warning(f'No vcf header for given {ftype} file')


def __get_vcf_header__(vcf_file: str):
    vcf_lines = __get_lines__(vcf_file)
    vcf_header = __get_vcf_header_from_lines__(vcf_lines)
    return vcf_header


def __get_vcf_header_from_lines__(vcf_lines: []):
    vcf_header = ""
    for line in vcf_lines:
        vcf_header = vcf_header + line
        if line.find("#CHROM") != -1:
            break
    return vcf_header


def __is_empty__(lines: []) -> bool:
    for line in lines:
        striped_line = line.strip()
        if striped_line != '' and not striped_line.startswith('#'):
            return False

    return True


def __create_unified_file__(files_lines: dict, output_path: str):
    """
    print the sv file complete (with header), then the cnv without a header
    and repeats with modified info section
    if sv file is empty prints all cnv and repeat lines, if cnv is also empty
    prints repeat lines
    """
    cnv_printed = False
    rep_printed = False
    with open(output_path, 'w+') as output_h:
        if files_lines['sv'] is not None:
            output_h.write("".join(files_lines['sv']))
        elif files_lines['cnv'] is not None:
            cnv_printed = True
            output_h.write("".join(filter(lambda l: __is_valid_line__(l), files_lines['cnv'])))
        elif files_lines['repeat'] is not None:
            rep_printed = True
            # separates the header and the content since repeat lines should be modified
            rep_header = __get_vcf_header_from_lines__(files_lines['repeat'])
            output_h.write(rep_header)
            __write_vcf_content__('repeat', files_lines, output_h)
        else:
            logging.warning('Empty/no vcf files to concatenate')
            return

        if files_lines['cnv'] is not None and not cnv_printed:
            __write_vcf_content__('cnv', files_lines, output_h)
        if files_lines['repeat'] is not None and not rep_printed:
            __write_vcf_content__('repeat', files_lines, output_h)

        output_h.flush()
        output_h.close()

    os.system(f'bgzip "{output_path}"')


def run(output_path: str, sv_path: str = None, cnv_path: str = None, repeat_path: str = None):
    output_file_path = output_path

    struct_files = {
        'sv': sv_path,
        'cnv': cnv_path,
        'repeat': repeat_path
    }
    struct_lines = {}

    for file_type in struct_files.keys():
        struct_lines[file_type] = None

        if struct_files[file_type] is None:
            logging.warning(f'Can\'t unified file type "{file_type}". File not exists.')
            continue

        lines = __get_lines__(struct_files[file_type])
        if __is_empty__(lines):
            logging.warning(f'Can\'t unified file type "{file_type}". The file is empty or contains only headers.')
            continue

        struct_lines[file_type] = lines

    __create_unified_file__(struct_lines, output_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-o', '--outputPath', help='the unified output VCF path (required)', required=True)
    parser.add_argument('-s', '--svPath', help='SV input file path (optional)', required=False, default=None)
    parser.add_argument('-c', '--cnvPath', help='CNV input file path (optional)', required=False, default=None)
    parser.add_argument('-r', '--repeatPath', help='Repeat input file path (optional)', required=False, default=None)

    args = parser.parse_args()
    run(args.outputPath, args.svPath, args.cnvPath, args.repeatPath)
