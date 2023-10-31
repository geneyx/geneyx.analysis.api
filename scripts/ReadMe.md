## ga.config.yml
This configuration file needs to be placed in the directory with the other python scripts. It serves as a reference to the account configuration. This configuration file specifies:
1.	Server: 'http://analysis.geneyx.com'
2.	apiUserId
3.	apiUserKey

The apiUserId and apiUserKey can be provided by contacting support@geneyx.com. 

## ga_CreateCase.py
This script allows a user to create an analysis using existing VCF files in an account. The CreateCase_Data.json file is located in the templates directory and contains the data fields that can be used with this python script. Descriptions of the available fields can be found here: 

https://github.com/geneyx/geneyx.analysis.api/wiki/Create-Case. 

Below is an example of this script that is run from command line:

C:\geneyx.analysis.api-main\scripts>python ga_CreateCase.py --data "C:\CreateCase_Data.json"

This would create a create a case in the account with the information derived from the json file. 


## ga_addClinicalRecord.py

This python script allows the user to add a clinical record to an existing subject. The clinicalRecord.json file can be modified with the specific information and executed with the script. For the phenotypic codes, only "HP:" terms can be entered. Descripton of the fields can be found here: 

https://github.com/geneyx/geneyx.analysis.api/wiki/AddClinicalRecord

Here is an example of the script being executed in command line:

C:\geneyx.analysis.api-main\scripts>python ga_addClinicalRecord.py --data "C:\clinicalRecord.json"

## ga_createPatient.py
This python script is used to create a new subject. The patient.json file contains the available fields and the description for the fields can be found here:

https://github.com/geneyx/geneyx.analysis.api/wiki/CreatePatient

Below is an example of this script that is run from command line:

C: \geneyx.analysis.api-main\scripts>python ga_CreateCase.py --data "C:\ Patient.json"

## ga_uploadSample_json.py
This python script enables a user to upload a VCF sample into a new or existing Subject with associated patient information. The data file is the sample.json file located in the template directory. Descriptions of the fields can be found here:

https://github.com/geneyx/geneyx.analysis.api/wiki/Create-Sample

To run this command the following fields need to be specified:
--snvVCF
--svVCF
--cnvVCF

An example of this command would be:

C:\geneyx.analysis.api-main\scripts>python ga_uploadSample_json.py --data "C:\sample.json" --snvVcf "C:\UpNew.vcf.gz"




