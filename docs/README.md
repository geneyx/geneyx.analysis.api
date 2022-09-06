# geneyx.analysis.api
This repository holds the scripts and manuals for Geneyx Analysis API:

https://github.com/geneyx/geneyx.analysis.api/



# Who needs geneyx anlysis API?
If you are Geneyx Analysis user and want to automate your data flow, for example:
•	Integrate your sequencing machine and automatically send FASTQ to Geneyx Analysis
•	Integrate with your LIMS and automatically create VCF samples or download reports
•	Integrate with your EMR and uploading clinical data to the patient record


# Examples

## Uploading sample to Geneyx Analysis

To run this code, you will need to navigate to https://github.com/geneyx/geneyx.analysis.api/. 
There is a green icon for Code. Select the icon and click Download Zip. Extract the files, then navigate 
to the script directory. 

The scripts directory contains:

- ga.config.yml
- ga_uploadSample.py
- UnifiedVcf.py

First you will need to modify the ga.config.yml file to reflect your provided api ID and api key. Once saved you can then define
the parameters which are present in the CreateSample.md file. 

## Unifying Dragen SV/CNV/Repeat files
Illumina's Dragen pipeline creates by default 4 types of VCF files
•	SNVs (Single Nucleotide Variant)
•	SV (Structural Variant)
•	CNV (Copy Number Variant)
•	Repeat
Uploading these files to Geneyx Analysis requires merging the SV/CNV/Repeat files and then uploading as a unified SV VCF file. 
For doing so one can use UnifiedVcf.py script. The script takes the three VCF files created by DRAGEN (SV/CNV/Repeats) and creates a unified SV file.

# Running prerequisites:
1.	Python 3.9.
2.	bgzip

## Windows Installation
On windows it is required to install python and also related components for using the ga_uploadSamplesWin.py
1.	Install Python 
2.	From Admin command line
  -	python -m pip install --upgrade pip
  -	pip install PyYAML
  - pip install requests





