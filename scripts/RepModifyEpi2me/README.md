# modify_epi2me_repeats.py

This script processes a VCF file and modifies the INFO field for records where the ALT column contains 'STR'.
If the INFO field contains `SVTYPE=DUP`, it will be replaced with `SVTYPE=REP`. If `SVTYPE=REP` is not present, it will be added.

## Usage

```bash
python modify_epi2me_repeats.py --input_vcf <input.vcf> --output_vcf <output.vcf>
```

- `<input.vcf>`: Path to the input VCF file to process.
- `<output.vcf>`: Path where the processed VCF will be saved.

## Example

```bash
python modify_epi2me_repeats.py --input_vcf sample_input.vcf --output_vcf sample_output.vcf
```

This will read `sample_input.vcf`, process it, and write the result to `sample_output.vcf`.

## What it does
- For each VCF record (non-header line), if the ALT field contains 'STR':
  - If the INFO field contains `SVTYPE=DUP`, it is replaced with `SVTYPE=REP`.
  - If `SVTYPE=REP` is not present, it is added to the INFO field.
- All other lines are written unchanged.

## Requirements
- Python 3.x

No external dependencies are required.
