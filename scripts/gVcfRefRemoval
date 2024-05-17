#!/bin/bash

# Check for correct number of arguments
if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 <input_vcf_file> <output_vcf_file>"
    exit 1
fi

input_file="$1"
output_file="$2"

# Check if input file exists
if [[ ! -f "$input_file" ]]; then
    echo "Input file not found!"
    exit 1
fi

# Process the VCF file
awk '
BEGIN {
    OFS="\t";
}
# Preserve header lines
/^#/ {
    print;
    next;
}
{
    # Split the ALT field by comma
    split($5, alts, ",");

    # Create a new ALT field excluding <REF>
    new_alts = "";
    for (i in alts) {
        if (alts[i] != "<REF>") {
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

    # Update the ALT field
    $5 = new_alts;

    # Print the updated line
    print;
}' "$input_file" > "$output_file"

echo "Processing complete. Output written to $output_file"
