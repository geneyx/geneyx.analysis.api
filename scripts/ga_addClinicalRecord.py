import argparse
import requests
import ga_helperFunctions as funcs

#region Helper functions
# ---------------------------------

def _verifyRequiredFields(data):
    funcs.verifyFieldInData('SubjectId', data)
    #TODO: verify datetime correct
    funcs.verifyFieldInData('RecordDate', data)
    #TODO: is 'PhenotypeCodes' verification needed?

# --------------------------------
#endregion Helper functions

# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_addClinicalRecord.py', description='Creates a clinical record for a patient on Geneyx Analysis')
# Clinical-record data Json file
parser.add_argument('--data','-d', help = 'data JSON file', default='templates\clinicalRecord.json')
# commands (optional)
parser.add_argument('--config','-c', help = 'configuration file', default='ga.config.yml')
args = parser.parse_args()

#read the config file
config = funcs.loadYamlFile(args.config)
print(config)

#prepare the data to send
data = funcs.loadDataJson(args.data)
_verifyRequiredFields(data)
# add user connection fields
data['ApiUserKey'] = config['apiUserKey']
data['ApiUserID'] = config['apiUserId']
print(data)

# send request
api = config['server']+'/api/AddClinicalRecord'
print('Creating clinical record')
r = requests.post(api, json = data)
print(r)
print(r.content)