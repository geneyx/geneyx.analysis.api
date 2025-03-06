# Who needs geneyx analysis API?
If you are Geneyx Analysis user that want to automate your data flow, for example:
- Integrate your sequencing machine and automatically send FASTQ to Geneyx Analysis
- Integrate with your LIMS and automatically create VCF samples or download reports
- Integrate with your EMR and uploading clinical data to the patient record

The following items listed provide details for accomplishing these functions. If there is a feature that you would like to have, please contact support@geneyx.com. 

# Examples
## Uploading sample to Geneyx Analysis
For automating the process of uploading VCFs to Geneyx Analysis you can use the two files
scripts/ga.config.yml  			- request api key and user key from Geneyx Support edit the file and enter to the right places
scripts/ga_uploadSamples.py		- A python script that does the upload processing together with sample and patient data. please run it and check the command line arguments.
You can read more at docs/geneyx.analysis.api.pdf
scripts/ga_uploadSamplesWin.py  - The windows version of previous script since some component changed on windows


## Unifying Dragen SV/CNV/Repeat files
Illumina's Dragen pipeline creates by default 4 types of VCF files
* SNVs
* SV/CNV/Repeat
for uploading those files to Geneyx Analysis it is required to merge the SV/CNV/Repeat files and upload the merged file as unified SV.
For doing so one can use scripts/UnifiedVcf.py
The script takes as parameters the three VCF files created by DRAGEN SV/CNV/Repeats and creates a unified SV file. 

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
 