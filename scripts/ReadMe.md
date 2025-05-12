# ga.config.yml
This configuration file needs to be placed in the directory with the other python scripts. It serves as a reference to the account configuration. This configuration file specifies:
1.	Server: 'https://analysis.geneyx.com'
2.	apiUserId
3.	apiUserKey

The apiUserId and apiUserKey can be provided by contacting support@geneyx.com. 

# ga_CreateCase.py
This script allows a user to create an analysis using existing VCF files in an account. The CreateCase_Data.json file is located in the templates directory and contains the data fields that can be used with this python script. Descriptions of the available fields can be found here: 

https://github.com/geneyx/geneyx.analysis.api/wiki/Create-Case. 

Below is an example of this script that is run from command line:

C:\geneyx.analysis.api-main\scripts>python ga_CreateCase.py --data "C:\CreateCase_Data.json"

This would create a create a case in the account with the information derived from the json file. 


# ga_addClinicalRecord.py

This python script allows the user to add a clinical record to an existing subject. The clinicalRecord.json file can be modified with the specific information and executed with the script. For the phenotypic codes, only "HP:" terms can be entered. Descripton of the fields can be found here: 

https://github.com/geneyx/geneyx.analysis.api/wiki/AddClinicalRecord

Here is an example of the script being executed in command line:

C:\geneyx.analysis.api-main\scripts>python ga_addClinicalRecord.py --data "C:\clinicalRecord.json"

# ga_createPatient.py
This python script is used to create a new subject. The patient.json file contains the available fields and the description for the fields can be found here:

https://github.com/geneyx/geneyx.analysis.api/wiki/CreatePatient

Below is an example of this script that is run from command line:

C: \geneyx.analysis.api-main\scripts>python ga_CreateCase.py --data "C:\ Patient.json"

# ga_uploadSample_json.py
This python script enables a user to upload a VCF sample into a new or existing Subject with associated patient information. The data file is the sample.json file located in the template directory. Descriptions of the fields can be found here:

[https://github.com/geneyx/geneyx.analysis.api/wiki/Create-Sample](https://github.com/geneyx/geneyx.analysis.api/wiki/Upload-Sample)

To run this command the following fields need to be specified:
--snvVCF
--svVCF
--cnvVCF

An example of this command would be:

C:\geneyx.analysis.api-main\scripts>python ga_uploadSample_json.py --data "C:\sample.json" --snvVcf "C:\UpNew.vcf.gz"

# ga_uploadBatch.py
This script allows a user to initiate a batch upload via command line into a secondary pipeline of Geneyx using the BatchImportTemplate.txt file, located in the template directory (https://github.com/geneyx/geneyx.analysis.api/blob/main/scripts/templates/BatchImportTemplate.txt). To run this, a Data Source must be configured in your Geneyx account, which can be accessed in the Settings dialog of the application. 
Below is an example of this script that is run from command line:

C:\geneyx.analysis.api-main\scripts>python ga_uploadBatch.py --batchFile "C:\Geneyx\geneyx.analysis.api-main\scripts\BatchImportTemplate.txt"

This would iniate a batch upload of fastq files into the secondary pipeline of Geneyx following the data specified in BatchImportTemplate.txt. 


# gVcfMod.sh: VCF File Processing Script

## Overview
The `gVcfMod.sh` script is designed to process **VCF (Variant Call Format)** files by removing the `<REF>` and `<NON_REF>` entries from the **ALT field** in the VCF file. The script works with both **gzipped** (`.vcf.gz`) and **uncompressed** `.vcf` files, preserving the header lines and modifying the variant data.

## Prerequisites
To run the script, you need the following:
- **Bash**: A Unix-like environment (Linux, macOS, or **WSL** on Windows).
- **AWK**: For processing the VCF data.
- **zcat** or **gzip**: For decompressing gzipped files on the fly.
- **dos2unix**: If you're on **Windows** (via WSL or Cygwin), you may need to convert line endings from Windows to Unix style.

### Install `dos2unix` (Windows Users)
If you're using Windows and encounter issues with line endings (e.g., `^M` errors), you can install and use `dos2unix` to convert the script's line endings to Unix-style.

To install `dos2unix` on WSL:

```bash```
sudo apt-get install dos2unix

Once installed, you can convert the script file:
```bash```
dos2unix gVcfMod.sh

This command will convert the line endings from Windows-style (CRLF) to Unix-style (LF).

###  Usage
Step 1: Prepare the Files
Ensure you have the following:

Input VCF file (either gzipped or uncompressed).

Output file where the processed VCF data will be saved.

Step 2: Run the Script
To use the script, execute the following command in your Bash terminal:

```bash```
./gVcfMod.sh <input_vcf_file> <output_vcf_file>

Where:

<input_vcf_file> is the path to your input VCF file (either .vcf or .vcf.gz).

<output_vcf_file> is the path to the output file that will contain the processed VCF data.

Step 3: Check the Output
After the script finishes running, the modified VCF file will be saved to the specified output file (modified.vcf in the example).

### Script Details
What the Script Does:
Preserves header lines: Lines starting with # are preserved as-is (they contain metadata and column names).

Removes <REF> and <NON_REF> from the ALT field: If these entries exist in the ALT field (column 5), they will be removed.

Skips variants with no alternate alleles left: If the ALT field becomes empty after removing <REF> and <NON_REF>, that variant is skipped.

Supports gzipped VCF files: The script can process gzipped (.vcf.gz) files using zcat or gzip.

What to Expect After Running:
The script will produce a new VCF file where:

The <REF> and <NON_REF> values are removed from the ALT field.

The header lines are retained.

Variants with no remaining alternate alleles are skipped.

