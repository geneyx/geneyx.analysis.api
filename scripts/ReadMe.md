##Scripts 
## ga.config.yml
This configuration files needs to be placed in the directory with the other python scripts. It serves as a reference to the account configuration. This configuration file specifies:
1.	Server: 'http://analysis.geneyx.com'
2.	apiUserId
3.	apiUserKey

The apiUserId and apiUserKey can be provided by contacting support@geneyx.com. 

## ga_CreateCase.py
This script allows a user to create an analysis using existing VCF files in an account. The CreateCase_Data.json file is located in the templates directory and contains the data fields that can be used with this python script. Descriptions of the available fields can be found here: https://github.com/geneyx/geneyx.analysis.api/wiki/Create-Case. 

Below is an example of this script that is run from command line:

C:\Users\eliws\geneyx.analysis.api-main\scripts>python ga_CreateCase.py --data "C:\Users\eliws\ CreateCase_Data.json"
This would create a create a case in the account with the information derived from the json file. 
