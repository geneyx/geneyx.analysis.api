#!/usr/bin/env python3
"""
Minimal CLI wrapper that takes a JSON file (matching your 'entries' schema)
and uploads via your existing uploader_with_unify.py.

Usage:
  python vcf_uploader_from_json.py --json Geneyx_VCF_Upload.json --config ga.config.yml
  python vcf_uploader_from_json.py --json Geneyx_VCF_Upload.json --config ga.config.yml --dry-run
  python vcf_uploader_from_json.py --json Geneyx_VCF_Upload.json --config ga.config.yml --retries 3 --log upload_log.txt
"""

import argparse
import json
import os
import subprocess
import sys
import time

def parse_args():
    p = argparse.ArgumentParser(
        description="Upload Geneyx entries from JSON (no GUI)."
    )
    p.add_argument("--json", required=True, help="Path to JSON file with {'entries': [...]} payload.")
    p.add_argument("--config", required=True, help="Path to ga.config.yml.")
    p.add_argument("--uploader", default="uploader_with_unify.py",
                   help="Path to the existing uploader script (default: uploader_with_unify.py).")
    p.add_argument("--dry-run", action="store_true",
                   help="Validate and show a brief summary, but do not upload.")
    p.add_argument("--retries", type=int, default=1,
                   help="How many times to retry on failure (default: 1 = no retry).")
    p.add_argument("--retry-wait", type=float, default=2.0,
                   help="Seconds to wait between retries (default: 2.0).")
    p.add_argument("--log", default=None,
                   help="Optional log file path. If omitted, prints to stdout/stderr.")
    return p.parse_args()

def load_entries(json_path):
    if not os.path.isfile(json_path):
        sys.exit(f"[ERROR] JSON file not found: {json_path}")
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        sys.exit(f"[ERROR] Failed to read JSON: {e}")

    if not isinstance(data, dict) or "entries" not in data or not isinstance(data["entries"], list):
        sys.exit("[ERROR] JSON must be an object with an 'entries' array.")

    # Light sanity checks per your converter’s output:
    problems = []
    for i, entry in enumerate(data["entries"], 1):
        if not isinstance(entry, dict):
            problems.append(f"Entry #{i} is not an object.")
            continue
        # Proband row should have sampleSerialNumber (your converter always keeps it)
        if not entry.get("sampleSerialNumber"):
            problems.append(f"Entry #{i} missing 'sampleSerialNumber'.")
        # Optional but recommended:
        if not entry.get("genomeBuild"):
            problems.append(f"Entry #{i} missing 'genomeBuild'.")
    if problems:
        for msg in problems:
            print(f"[WARN] {msg}")
    return data

def summarize(data):
    n = len(data["entries"])
    trio_like = sum(1 for e in data["entries"] if "AssociatedSamples" in e and e["AssociatedSamples"])
    singleton_like = n - trio_like
    # Count VCF presence
    def has(e, k): return 1 if e.get(k) else 0
    snv = sum(has(e,"snvVcf") for e in data["entries"])
    sv = sum(has(e,"svVcf") for e in data["entries"])
    cnv = sum(has(e,"cnvVcf") for e in data["entries"])
    rpt = sum(has(e,"repeatVcf") for e in data["entries"])
    print(f"[INFO] Entries: {n} (Singleton-like: {singleton_like}, Trio-like: {trio_like})")
    print(f"[INFO] VCF coverage across entries: SNV={snv}, SV={sv}, CNV={cnv}, REPEAT={rpt}")

def run_uploader(uploader, json_path, config_path, log_path=None, retries=1, retry_wait=2.0):
    cmd = ["python", uploader, "--json", json_path, "--config", config_path]

    attempt = 0
    while attempt < max(1, retries):
        attempt += 1
        print(f"[INFO] Running uploader (attempt {attempt}/{retries})...")
        try:
            if log_path:
                with open(log_path, "a") as logf:
                    logf.write(f"\n--- Attempt {attempt} ---\n")
                    result = subprocess.run(cmd, stdout=logf, stderr=logf, text=True, check=True)
            else:
                result = subprocess.run(cmd, check=True)
            print("[INFO] Upload succeeded.")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Upload failed (attempt {attempt}). Return code: {e.returncode}")
            if attempt < retries:
                print(f"[INFO] Waiting {retry_wait} seconds before retry...")
                time.sleep(retry_wait)
            else:
                print("[ERROR] All attempts failed.")
                return e.returncode

def main():
    args = parse_args()

    # Basic file existence checks
    if not os.path.isfile(args.config):
        sys.exit(f"[ERROR] Config file not found: {args.config}")
    if not os.path.isfile(args.uploader):
        sys.exit(f"[ERROR] Uploader script not found: {args.uploader}")

    data = load_entries(args.json)
    summarize(data)

    if args.dry_run:
        print("[DRY-RUN] No upload performed.")
        if args.log:
            with open(args.log, "a") as logf:
                logf.write("[DRY-RUN] Summary complete. No upload performed.\n")
        return 0

    return_code = run_uploader(
        uploader=args.uploader,
        json_path=args.json,
        config_path=args.config,
        log_path=args.log,
        retries=args.retries,
        retry_wait=args.retry_wait
    )
    sys.exit(return_code if return_code is not None else 0)

if __name__ == "__main__":
    main()
