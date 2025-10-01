# Geneyx JSON Uploader — README

This folder contains a lightweight, JSON‑first workflow for uploading samples and trios into **Geneyx Analysis**. It assumes you already have VCFs (SNV/SV/CNV/Repeat/TRGT) and a prepared JSON payload.

> **TL;DR**  
> 1) Edit `ga.config.yml` with your API keys.  
> 2) Put your JSON at `example_json.json` (or any path).  
> 3) Run:  
>    ```bash
>    python vcf_uploader_from_json.py --json example_json.json --config ga.config.yml --dry-run
>    python vcf_uploader_from_json.py --json example_json.json --config ga.config.yml --retries 3 --log upload_log.txt
>    ```

---

## Contents

- **`uploader_with_unify.py`** – Main uploader that authenticates with Geneyx and performs optional VCF unification when needed (e.g., TRGT present; SV+CNV+Repeat).  
- **`vcf_uploader_from_json.py`** – Minimal CLI wrapper that accepts a **JSON file with `entries`** and calls `uploader_with_unify.py` under the hood.  
- **`example_json.json`** – Example customer‑ready JSON showing one singleton and one trio.  
- **`ga.config.yml`** – Your credentials and defaults (edit this).  
- **`ga_helperFunctions.py`** – Shared helpers imported by the uploader.  
- **`unify_vcf.py`** – *Legacy/optional.* Only needed if your uploader relies on the external module. Current builds do **not** require this as unification is internal to `uploader_with_unify.py`.

> **Do I need `unify_vcf.py`?**  
> No for current versions. Keep it only for backward compatibility. The uploader will log if it expects an external `unify_vcf.py`.

---

## Requirements

- **Python** 3.9+  
- Packages:
  ```bash
  pip install pandas openpyxl requests pyyaml
  ```
- Network access to `https://analysis.geneyx.com`

> Tip (Windows PowerShell):  
> ```powershell
> py -3 -m pip install pandas openpyxl requests pyyaml
> ```

---

## Configure

Edit **`ga.config.yml`** (example):
```yaml
apiUserId: "YOUR_API_USER_ID"
apiUserKey: "YOUR_API_USER_KEY"
```

- `apiUserId` / `apiUserKey`: Required for API authentication.  

---

## JSON Format

The uploader expects a single file containing a top‑level **`entries`** array. Each element is a **sample**.  
- For **trios**, include **only the proband** as an entry, and embed parents within **`AssociatedSamples`**.  
- You may include any subset of `snvVcf`, `svVcf`, `cnvVcf`, `repeatVcf`.  
- Dates should be **`YYYY/MM/DD`**.  
- `genomeBuild` should match your account (e.g., `hg38`).  
- `ProtocolId` and `kitId` must correspond to values available in your Geneyx account.

### Minimal Singleton Example
```json
{
  "entries": [
    {
      "sampleSerialNumber": "SNG-001a",
      "SubjectId": "SNG-001a",
      "snvVcf": "C:/path/to/singleton_abcdefg.snv.vcf.gz",
      "genomeBuild": "hg38",
      "sampleTarget": "WholeGenome",
      "ProtocolId": "RG_SNV_SV",
      "kitId": "LongRead Intergenic Boston Test",
      "patientGender": "F",
      "SubjectName": "Jane Example",
      "SubjectDateOfBirth": "1997/05/22",
      "sampleRelation": "Proband"
    }
  ]
}
```

### Trio Example (Proband + Embedded Parents)
```json
{
  "entries": [
    {
      "sampleSerialNumber": "TRIO-PRO-001",
      "SubjectId": "TRIO-PRO-001",
      "snvVcf": "C:/path/to/proband_abce.snv.vcf.gz",
      "svVcf": "C:/path/to/proband_abce.sv.vcf.gz",
      "cnvVcf": "C:/path/to/proband_abce.cnv.vcf.gz",
      "repeatVcf": "C:/path/to/proband_abce.trgt.vcf.gz",
      "ProtocolId": "RG_TRIO",
      "kitId": "LongRead Intergenic Boston Test",
      "genomeBuild": "hg38",
      "sampleTarget": "WholeGenome",
      "patientGender": "M",
      "SubjectName": "Alex Proband",
      "SubjectDateOfBirth": "2019/11/03",
      "sampleRelation": "Proband",
      "AssociatedSamples": [
        {
          "Relation": "Mother",
          "SampleId": "TRIO-MAT-001",
          "snvVcf": "C:/path/to/mother_abce.snv.vcf.gz",
          "svVcf": "C:/path/to/mother_abce.sv.vcf.gz",
          "cnvVcf": "C:/path/to/mother_abce.cnv.vcf.gz",
          "repeatVcf": "C:/path/to/mother_abce.trgt.vcf.gz",
          "kitId": "LongRead Intergenic Boston Test",
          "Affected": "Unaffected"
        },
        {
          "Relation": "Father",
          "SampleId": "TRIO-PAT-001",
          "snvVcf": "C:/path/to/father_abce.snv.vcf.gz",
          "svVcf": "C:/path/to/father_abce.sv.vcf.gz",
          "cnvVcf": "C:/path/to/father_abce.cnv.vcf.gz",
          "repeatVcf": "C:/path/to/father_abce.trgt.vcf.gz",
          "kitId": "LongRead Intergenic Boston Test",
          "Affected": "Unaffected"
        }
      ]
    }
  ]
}
```

> **Phenotypes:** You may provide HPO IDs and/or free text (comma‑separated), e.g.  
> `"Phenotypes": "HP:0000189,\"Narrow palate\", \"Thin upper lip vermilion\"",`

---

## Usage

### 1) Validate Only (Dry‑Run)
```bash
python vcf_uploader_from_json.py --json example_json.json --config ga.config.yml --dry-run
```

### 2) Upload
```bash
python vcf_uploader_from_json.py --json example_json.json --config ga.config.yml
```

### 3) Upload with Retries & Logging
```bash
python vcf_uploader_from_json.py --json example_json.json --config ga.config.yml --retries 3 --log upload_log.txt
```

**What happens?**  
- The wrapper validates your JSON, summarizes entries, and invokes:  
  ```bash
  python uploader_with_unify.py --json example_json.json --config ga.config.yml
  ```
- If present, the uploader may unify SV/CNV/Repeat into a single VCF as required by Geneyx.

---

## Return Codes & Logs

- **0** – Success  
- **Non‑zero** – One or more failures reported by the uploader

If `--log upload_log.txt` is provided, all stdout/stderr from the uploader are appended to that file.

---

## Troubleshooting

- **Auth error / 401 / 403**  
  - Verify `apiUserId` and `apiUserKey` in `ga.config.yml`.  
  - Ensure your IP/network is allowed by your organization.

- **“Protocol/Kit not found”**  
  - Use values existing in your Geneyx account. If unsure, ask your admin for the correct `ProtocolId` and `kitId`.

- **“Unified VCF required”** or repeat/TRGT present  
  - Current `uploader_with_unify.py` handles it internally. If you see import/file errors for `unify_vcf.py`, you are on an older version—place `unify_vcf.py` next to the uploader or upgrade the uploader.

- **File not found**  
  - Check local/UNC/S3 paths. For S3 presigned URLs, ensure they’re valid during the upload window.

- **Date parsing**  
  - Use `YYYY/MM/DD` format for `SubjectDateOfBirth`, `sampleTakenDate`, etc.

---

## FAQ

**Q: Can I omit `svVcf`, `cnvVcf`, or `repeatVcf`?**  
A: Yes. Include whatever you have; the uploader will handle presence/absence appropriately.

**Q: Do parents need full metadata?**  
A: Only include the VCF paths you want uploaded and optional `kitId`. Full subject‑level fields for parents are not required when embedded under `AssociatedSamples`.

**Q: Windows vs Linux paths?**  
A: Both are supported. Use `C:/...` on Windows or `/data/...` on Linux. Network paths like `\\\\server\\share\\...` also work.

---

## Support

- Reach out to your Geneyx representative or support channel with:
  - Your `upload_log.txt` (if available)
  - The JSON you attempted to upload (redact PHI if needed)
  - A brief description of your environment (OS, Python version)

---

**© 2025 Geneyx — Internal tools & examples for customer onboarding.**
