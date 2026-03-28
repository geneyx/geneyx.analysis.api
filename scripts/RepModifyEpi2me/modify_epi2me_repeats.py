import argparse

def process_vcf(input_vcf, output_vcf):
    with open(input_vcf, 'r') as infile, open(output_vcf, 'w') as outfile:
        for line in infile:
            if line.startswith('#'):
                outfile.write(line)
                continue
            fields = line.strip().split('\t')
            if len(fields) < 8:
                outfile.write(line)
                continue
            alt = fields[4]
            info = fields[7]
            if 'STR' in alt:
                if 'SVTYPE=DUP' in info:
                    info = info.replace('SVTYPE=DUP', 'SVTYPE=REP')
                elif 'SVTYPE=REP' not in info:
                    if info == '.' or info == '':
                        info = 'SVTYPE=REP'
                    else:
                        info += ';SVTYPE=REP'
                fields[7] = info
                line = '\t'.join(fields) + '\n'
            outfile.write(line)

def main():
    parser = argparse.ArgumentParser(description='Add SVTYPE=REP to INFO if ALT contains STR in VCF.')
    parser.add_argument('--input_vcf', help='Input VCF file')
    parser.add_argument('--output_vcf', help='Output VCF file')
    args = parser.parse_args()

    process_vcf(args.input_vcf, args.output_vcf)
    print(f'Processed VCF saved to: {args.output_vcf}')

if __name__ == '__main__':
    main()
