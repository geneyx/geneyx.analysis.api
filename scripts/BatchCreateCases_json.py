import json
import argparse
import requests
import ga_helperFunctions as funcs

#region Helper functions
# ---------------------------------

def _verifyRequiredFields(data):
    funcs.verifyFieldInData('ProtocolId', data)
    funcs.verifyFieldInData('SubjectId', data)
    funcs.verifyFieldInData('ProbandSampleId', data)
    
# --------------------------------
#endregion Helper functions

# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_createCase.py', description='Creates a case on Geneyx Analysis')
# Case data JSON file
parser.add_argument('--data', '-d', help='data JSON file', default='templates/case.json')
# commands (optional)
parser.add_argument('--config', '-c', help='configuration file', default='ga.config.yml')
args = parser.parse_args()

# Read the config file
config = funcs.loadYamlFile(args.config)
print(config)

# Prepare the data to send
data_list = funcs.loadDataJson(args.data)
if not isinstance(data_list, list):
    raise ValueError("The data JSON file must contain a list of samples")

for data in data_list:
    _verifyRequiredFields(data)
    # Add user connection fields
    data['ApiUserKey'] = config['apiUserKey']
    data['ApiUserID'] = config['apiUserId']
    print(data)

    # Send request
    api = config['server'] + '/api/CreateCase'
    print('Creating case')
    r = requests.post(api, json=data)
    print(r)
    print(r.content)
