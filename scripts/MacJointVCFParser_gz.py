import sys
import os
import gzip

if len(sys.argv) != 3:
    print("Usage: python script.py <input_vcf_file> <output_directory>")
    sys.exit(1)

input_vcf_file = sys.argv[1]
output_directory = sys.argv[2]

# Ensure the output directory exists, create it if necessary
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to open VCF file (supports both plain and gzipped files)
def open_vcf(file_path):
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')
    else:
        return open(file_path, 'r')

# Open the joint VCF file for reading
with open_vcf(input_vcf_file) as joint_vcf:
    # Read header lines to extract sample names
    header_lines = []
    sample_names = []
    for line in joint_vcf:
        if line.startswith('#CHROM'):
            header_lines.append(line)
            sample_names = line.strip().split('\t')[9:]
            break
        header_lines.append(line)

# Generate output VCF filenames based on sample names and input filename
base_filename = os.path.splitext(os.path.basename(input_vcf_file))[0]
if base_filename.endswith('.vcf'):
    base_filename = base_filename[:-4]
output_vcf_files = [os.path.join(output_directory, f'{base_filename}_{sample}.vcf') for sample in sample_names]

# Open the joint VCF file again
with open_vcf(input_vcf_file) as joint_vcf:
    # Open the output files for writing
    out_files = [open(output_vcf, 'w') for output_vcf in output_vcf_files]

    # Write header lines to each output file
    for out_file in out_files:
        out_file.writelines(header_lines)

    # Process each line in the joint VCF file
    for line in joint_vcf:
        # Check if the line is a header line (starts with '#')
        if not line.startswith('#'):
            # Split the data fields in the line
            fields = line.split('\t')

            # Extract information for each individual (starting from the ninth column)
            individual_data = fields[9:]

            # Write the modified lines to the respective output files
            for i, out_file in enumerate(out_files):
                out_file.write('\t'.join(fields[:9] + [individual_data[i]] + fields[9+i+1:]))

# Close the output files
for out_file in out_files:
    out_file.close()
