import sys
import os
import gzip

# Simple message printer
def show_message(message):
    print(message)

# Check if the correct number of arguments is passed
if len(sys.argv) != 2:
    show_message(f"Incorrect number of arguments. Received: {len(sys.argv)}\nArguments: {sys.argv}")
    sys.exit(1)

input_vcf_file = sys.argv[1]

# Get the directory where the script is located
exe_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# Ensure the output directory exists
if not os.path.exists(exe_directory):
    os.makedirs(exe_directory)

show_message(f"Input file: {input_vcf_file}\nOutput directory: {exe_directory}")

# Function to open VCF file (supports both plain and gzipped files)
def open_vcf(file_path):
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')
    else:
        return open(file_path, 'r')

# Open the joint VCF file for reading
try:
    with open_vcf(input_vcf_file) as joint_vcf:
        header_lines = []
        sample_names = []
        for line in joint_vcf:
            if line.startswith('#CHROM'):
                header_lines.append(line)
                stripped_line = line.strip()
                columns = stripped_line.split('\t')
                if len(columns) >= 10:
                    sample_names = columns[9:]
                break
            elif line.startswith('##'):
                header_lines.append(line)
except Exception as e:
    show_message(f"Error opening or reading the input VCF file: {e}")
    sys.exit(1)

if not sample_names:
    show_message("Error: Sample names are still empty after processing the header.")
    sys.exit(1)

base_filename = os.path.splitext(os.path.basename(input_vcf_file))[0]
if base_filename.endswith('.vcf'):
    base_filename = base_filename[:-4]
output_vcf_files = [os.path.join(exe_directory, f'{base_filename}_{sample}.vcf.gz') for sample in sample_names]

show_message(f"Output VCF files will be generated at:\n" + '\n'.join(output_vcf_files))

try:
    with open_vcf(input_vcf_file) as joint_vcf:
        out_files = [gzip.open(output_vcf, 'wt') for output_vcf in output_vcf_files]

        for i, out_file in enumerate(out_files):
            for header in header_lines:
                out_file.write(header)

        for line in joint_vcf:
            if not line.startswith('#'):
                fields = line.strip().split('\t')

                if len(fields) < 10:
                    continue

                individual_data = fields[9:]

                if len(individual_data) != len(sample_names):
                    continue

                for i, out_file in enumerate(out_files):
                    out_file.write('\t'.join(fields[:9] + [individual_data[i]]) + '\n')

        for out_file in out_files:
            out_file.close()

    show_message("Processing complete!")
except Exception as e:
    show_message(f"Error processing the VCF file: {e}")
    sys.exit(1)
