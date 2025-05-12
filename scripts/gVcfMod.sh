#!/bin/bash

# Function to print usage
usage() {
    echo "Usage: $0 <input_vcf_file> <output_vcf_file>"
    exit 1
}

# Function to process the VCF file
process_vcf() {
    local input_file="$1"
    local output_file="$2"
    
    if [[ "$input_file" =~ \.gz$ ]]; then
        # If the input file is gzipped, decompress and process
        zcat "$input_file" | awk '
        BEGIN {
            OFS="\t"; # Set output field separator to tab
        }
        # Preserve header lines (those starting with #)
        /^#/ {
            print;
            next;
        }
        {
            # Split the ALT field by comma
            split($5, alts, ",");

            # Create a new ALT field excluding <REF> and <NON_REF>
            new_alts = "";
            for (i in alts) {
                if (alts[i] != "<REF>" && alts[i] != "<NON_REF>") {
                    if (new_alts != "") {
                        new_alts = new_alts "," alts[i];
                    } else {
                        new_alts = alts[i];
                    }
                }
            }

            # If new_alts is empty, skip this variant
            if (new_alts == "") {
                next;
            }

            # Update the ALT field with the new alternatives
            $5 = new_alts;

            # Print the updated line
            print;
        }
        ' > "$output_file"  # Process and redirect output to the output file
    else
        # If the file is not gzipped, process it directly
        awk '
        BEGIN {
            OFS="\t"; # Set output field separator to tab
        }
        # Preserve header lines (those starting with #)
        /^#/ {
            print;
            next;
        }
        {
            # Split the ALT field by comma
            split($5, alts, ",");

            # Create a new ALT field excluding <REF> and <NON_REF>
            new_alts = "";
            for (i in alts) {
                if (alts[i] != "<REF>" && alts[i] != "<NON_REF>") {
                    if (new_alts != "") {
                        new_alts = new_alts "," alts[i];
                    } else {
                        new_alts = alts[i];
                    }
                }
            }

            # If new_alts is empty, skip this variant
            if (new_alts == "") {
                next;
            }

            # Update the ALT field with the new alternatives
            $5 = new_alts;

            # Print the updated line
            print;
        }
        ' "$input_file" > "$output_file"  # Process and redirect output to the output file
    fi
}

# Check for correct number of arguments
if [[ "$#" -ne 2 ]]; then
    usage
fi

# Assign input and output file paths from arguments
input_file="$1"
output_file="$2"

# Check if the input file exists
if [[ ! -f "$input_file" ]]; then
    echo "Input file not found!"
    exit 1
fi

# Process the VCF file by calling the function
process_vcf "$input_file" "$output_file"

# Notify the user that the processing is complete
echo "Processing complete. Output written to $output_file"
