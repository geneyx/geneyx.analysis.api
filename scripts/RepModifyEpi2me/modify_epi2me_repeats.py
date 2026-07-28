import argparse
import gzip
from pathlib import Path
from typing import TextIO


def open_vcf(path: str, mode: str) -> TextIO:
    """
    Open either a plain-text VCF or gzip-compressed VCF.

    Supported modes:
      - 'rt' for reading text
      - 'wt' for writing text
    """
    if path.lower().endswith(".gz"):
        return gzip.open(path, mode, encoding="utf-8")
    return open(path, mode, encoding="utf-8")


def process_vcf(input_vcf: str, output_vcf: str) -> None:
    with open_vcf(input_vcf, "rt") as infile, open_vcf(output_vcf, "wt") as outfile:
        for line in infile:
            if line.startswith("#"):
                outfile.write(line)
                continue

            fields = line.rstrip("\n").split("\t")

            if len(fields) < 8:
                outfile.write(line)
                continue

            alt = fields[4]
            info = fields[7]

            if "STR" in alt:
                if "SVTYPE=DUP" in info:
                    info = info.replace("SVTYPE=DUP", "SVTYPE=REP")
                elif "SVTYPE=REP" not in info:
                    if info in ("", "."):
                        info = "SVTYPE=REP"
                    else:
                        info += ";SVTYPE=REP"

                fields[7] = info
                line = "\t".join(fields) + "\n"

            outfile.write(line)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add SVTYPE=REP to INFO when ALT contains STR."
    )
    parser.add_argument(
        "--input_vcf",
        required=True,
        help="Input VCF file, optionally gzip-compressed.",
    )
    parser.add_argument(
        "--output_vcf",
        required=True,
        help="Output VCF file, optionally gzip-compressed.",
    )
    args = parser.parse_args()

    if not Path(args.input_vcf).is_file():
        parser.error(f"Input file does not exist: {args.input_vcf}")

    process_vcf(args.input_vcf, args.output_vcf)
    print(f"Processed VCF saved to: {args.output_vcf}")


if __name__ == "__main__":
    main()
