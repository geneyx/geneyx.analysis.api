import gzip
import os
import logging
import shutil

def __get_lines__(file_path: str) -> []:
    try:
        with gzip.open(file_path, 'rt') as file_h:
            lines = file_h.readlines()
    except:
        with open(file_path) as file_h:
            lines = file_h.readlines()
    return lines

def __modify_repeat_line__(repeat_line: str) -> str:
    parts = repeat_line.strip().split("\t")
    if len(parts) < 9:
        return repeat_line
    info = parts[7]
    info += ';SVTYPE=REP'
    parts[7] = info
    return "\t".join(parts) + '\n'

def __modify_roh_line__(vcf_line) -> str:
    bed_data = vcf_line.strip().split('\t')
    pos_value = min([int(bed_data[1]), int(bed_data[2])]) + 1
    end_value = max([int(bed_data[1]), int(bed_data[2])])
    chromosome = bed_data[0]
    roh_score = bed_data[3]
    return f"{chromosome}\t{pos_value}\t.\tN\t<ROH>\t.\tPASS\tEND={end_value};SVTYPE=ROH;ROH_SCORE={roh_score}\tGT\t1/1\n"

def __is_valid_line__(line: str) -> bool:
    if line.startswith('#') or not line.strip():
        return True
    cells = line.strip().split('\t')
    if len(cells) < 9:
        return False
    info_cell = cells[7]
    format_key = cells[8]
    format_value = cells[9]
    if 'SVTYPE=' in info_cell:
        return True
    try:
        gt_index = format_key.split(':').index('GT')
        gt_value = format_value.split(':')[gt_index]
    except:
        return False
    return gt_value != '0' and gt_value != './.'

def __write_vcf_content__(ftype: str, lines_dict: dict, output_h, skip_svtype: bool):
    start = False if ftype != 'roh' else True
    for line in lines_dict[ftype]:
        if start:
            if ftype == 'repeat' and not skip_svtype:
                line = __modify_repeat_line__(line)
            elif ftype == 'roh':
                line = __modify_roh_line__(line)

            # Ensure newline at end
            output_h.write(line if line.endswith('\n') else line + '\n')

        if line.startswith('#CHROM'):
            start = True

    if not start:
        logging.warning(f'No vcf header for {ftype} file')

def __get_vcf_header_from_lines__(vcf_lines: []):
    header = ''
    for line in vcf_lines:
        header += line
        if line.startswith('#CHROM'):
            break
    return header

def __is_empty__(lines: []) -> bool:
    return all(line.strip() == '' or line.startswith('#') for line in lines)

def __sort_vcf__(vcf_file_path: str):
    with open(vcf_file_path, 'r') as infile:
        lines = infile.readlines()

    header_lines = [line for line in lines if line.startswith('#')]
    content_lines = [line for line in lines if not line.startswith('#')]

    # Fix: support POS field with float values like 32314000.0
    content_lines.sort(key=lambda x: (x.split('\t')[0], int(float(x.split('\t')[1]))))

    with open(vcf_file_path, 'w') as outfile:
        outfile.writelines(header_lines + content_lines)

    # Gzip the sorted file
    with open(vcf_file_path, 'rb') as f_in:
        with gzip.open(vcf_file_path + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(vcf_file_path)

def __create_unified_file__(files_lines: dict, output_path: str, skip_svtype: bool):
    cnv_printed = False
    rep_printed = False
    with open(output_path, 'w+') as output_h:
        if files_lines['sv']:
            output_h.write("".join(files_lines['sv']))
        elif files_lines['cnv'] is not None:
            cnv_printed = True
            for line in filter(__is_valid_line__, files_lines['cnv']):
                output_h.write(line if line.endswith('\n') else line + '\n')
        elif files_lines['repeat']:
            rep_printed = True
            output_h.write(__get_vcf_header_from_lines__(files_lines['repeat']))
            __write_vcf_content__('repeat', files_lines, output_h, skip_svtype)
        else:
            logging.warning('No valid input files')
            return

        if files_lines['cnv'] and not cnv_printed:
            __write_vcf_content__('cnv', files_lines, output_h, skip_svtype)
        if files_lines['repeat'] and not rep_printed:
            __write_vcf_content__('repeat', files_lines, output_h, skip_svtype)
        if files_lines['roh']:
            __write_vcf_content__('roh', files_lines, output_h, skip_svtype)

    __sort_vcf__(output_path)

def run(output_path: str, sv_path: str = None, cnv_path: str = None, repeat_path: str = None, roh_bed_path: str = None, skip_svtype: bool = False):
    struct_files = {
        'sv': sv_path,
        'cnv': cnv_path,
        'repeat': repeat_path,
        'roh': roh_bed_path
    }
    files_lines = {k: None for k in struct_files}

    for k, path in struct_files.items():
        if path and os.path.exists(path):
            lines = __get_lines__(path)
            if not __is_empty__(lines):
                files_lines[k] = lines
            else:
                logging.warning(f'{k} file is empty')
        elif path:
            logging.warning(f'{k} file does not exist: {path}')

    __create_unified_file__(files_lines, output_path, skip_svtype)
