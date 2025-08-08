import pandas as pd
import gzip
import argparse

def cnv_to_vcf(input_file, output_file):
    # Define the column names for the input TSV file
    columns = ["#sample", "chrm", "start", "end", "sv_type", "length", "DELLY_filter", "DELLY_sv_type",
               "DELLY_GT", "DELLY_DR", "DELLY_DV", "DELLY_RR", "DELLY_RV", "DELLY_CN", "DELLY_ovlp",
               "DELLY_count", "DELLY_boundary", "DELLY_merged", "MANTA_filter", "MANTA_sv_type",
               "MANTA_GT", "MANTA_PR", "MANTA_SR", "MANTA_GQ", "MANTA_PL", "MANTA_event", "MANTA_ovlp",
               "MANTA_count", "MANTA_boundary", "MANTA_merged", "method"]

    # Read the gzipped TSV file
    with gzip.open(input_file, 'rt') as f:
        df = pd.read_csv(f, sep='\t', names=columns, comment='#')

    # Create a VCF header
    vcf_header = [
        "##fileformat=VCFv4.2",
        "##source=CNV_converter",
        "##INFO=<ID=SVTYPE,Number=1,Type=String,Description=\"Type of structural variant\">",
        "##INFO=<ID=END,Number=1,Type=Integer,Description=\"End position of the variant\">",
        "##INFO=<ID=LEN,Number=1,Type=Integer,Description=\"Length of the variant\">",
        "##INFO=<ID=DELLY_filter,Number=.,Type=String,Description=\"DELLY filter status\">",
        "##INFO=<ID=DELLY_sv_type,Number=.,Type=String,Description=\"DELLY structural variant type\">",
        "##INFO=<ID=DELLY_GT,Number=.,Type=String,Description=\"DELLY genotype\">",
        "##INFO=<ID=DELLY_DR,Number=.,Type=Integer,Description=\"DELLY read depth\">",
        "##INFO=<ID=DELLY_DV,Number=.,Type=Integer,Description=\"DELLY variant depth\">",
        "##INFO=<ID=DELLY_RR,Number=.,Type=Integer,Description=\"DELLY reference read count\">",
        "##INFO=<ID=DELLY_RV,Number=.,Type=Integer,Description=\"DELLY variant read count\">",
        "##INFO=<ID=DELLY_CN,Number=.,Type=Integer,Description=\"DELLY copy number\">",
        "##INFO=<ID=DELLY_ovlp,Number=.,Type=String,Description=\"DELLY overlap\">",
        "##INFO=<ID=DELLY_count,Number=.,Type=Integer,Description=\"DELLY count\">",
        "##INFO=<ID=DELLY_boundary,Number=.,Type=String,Description=\"DELLY boundary\">",
        "##INFO=<ID=DELLY_merged,Number=.,Type=String,Description=\"DELLY merged\">",
        "##INFO=<ID=MANTA_filter,Number=.,Type=String,Description=\"MANTA filter status\">",
        "##INFO=<ID=MANTA_sv_type,Number=.,Type=String,Description=\"MANTA structural variant type\">",
        "##INFO=<ID=MANTA_GT,Number=.,Type=String,Description=\"MANTA genotype\">",
        "##INFO=<ID=MANTA_PR,Number=.,Type=Integer,Description=\"MANTA paired-end read count\">",
        "##INFO=<ID=MANTA_SR,Number=.,Type=Integer,Description=\"MANTA split-read count\">",
        "##INFO=<ID=MANTA_GQ,Number=.,Type=Integer,Description=\"MANTA genotype quality\">",
        "##INFO=<ID=MANTA_PL,Number=.,Type=String,Description=\"MANTA phred-scaled genotype likelihoods\">",
        "##INFO=<ID=MANTA_event,Number=.,Type=String,Description=\"MANTA event\">",
        "##INFO=<ID=MANTA_ovlp,Number=.,Type=String,Description=\"MANTA overlap\">",
        "##INFO=<ID=MANTA_count,Number=.,Type=Integer,Description=\"MANTA count\">",
        "##INFO=<ID=MANTA_boundary,Number=.,Type=String,Description=\"MANTA boundary\">",
        "##INFO=<ID=MANTA_merged,Number=.,Type=String,Description=\"MANTA merged\">",
        "##INFO=<ID=method,Number=.,Type=String,Description=\"Detection method\">",
        "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample"
    ]

    # Create a list to hold the VCF body lines
    vcf_body = []

    for index, row in df.iterrows():
        info = [
            f"SVTYPE={row['sv_type']}",
            f"END={row['end']}",
            f"LEN={row['length']}",
            f"DELLY_filter={row['DELLY_filter']}",
            f"DELLY_sv_type={row['DELLY_sv_type']}",
            f"DELLY_GT={row['DELLY_GT']}",
            f"DELLY_DR={row['DELLY_DR']}",
            f"DELLY_DV={row['DELLY_DV']}",
            f"DELLY_RR={row['DELLY_RR']}",
            f"DELLY_RV={row['DELLY_RV']}",
            f"DELLY_CN={row['DELLY_CN']}",
            f"DELLY_ovlp={row['DELLY_ovlp']}",
            f"DELLY_count={row['DELLY_count']}",
            f"DELLY_boundary={row['DELLY_boundary']}",
            f"DELLY_merged={row['DELLY_merged']}",
            f"MANTA_filter={row['MANTA_filter']}",
            f"MANTA_sv_type={row['MANTA_sv_type']}",
            f"MANTA_GT={row['MANTA_GT']}",
            f"MANTA_PR={row['MANTA_PR']}",
            f"MANTA_SR={row['MANTA_SR']}",
            f"MANTA_GQ={row['MANTA_GQ']}",
            f"MANTA_PL={row['MANTA_PL']}",
            f"MANTA_event={row['MANTA_event']}",
            f"MANTA_ovlp={row['MANTA_ovlp']}",
            f"MANTA_count={row['MANTA_count']}",
            f"MANTA_boundary={row['MANTA_boundary']}",
            f"MANTA_merged={row['MANTA_merged']}",
            f"method={row['method']}"
        ]

        vcf_body.append(f"{row['chrm']}\t{row['start']}\t.\tN\t<{row['sv_type']}>\t.\t.\t{';'.join(info)}\tGT\t0/1")

    # Write the VCF file as gzipped
    with gzip.open(output_file, 'wt') as f:
        for line in vcf_header:
            f.write(line + '\n')
        for line in vcf_body:
            f.write(line + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CNV TSV to VCF.")
    parser.add_argument("input_file", help="Path to the input gzipped TSV file.")
    parser.add_argument("output_file", help="Path to the output gzipped VCF file.")
    args = parser.parse_args()

    cnv_to_vcf(args.input_file, args.output_file)
