import argparse
import requests
import ga_helperFunctions as funcs

#region Helper functions
# ---------------------------------

def _verifyRequiredFields(data):
    funcs.verifyFieldInData('sampleSn', data)    

# --------------------------------
#endregion Helper functions

# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_addQcData.py', description='Updates a QC data for a sample on Geneyx Analysis')
# QC data Json file
parser.add_argument('--data','-d', help = 'data JSON file', default='templates\qcData.json')
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
api = config['server']+'/api/UpdateSampleSequencingQc'
print('Updating QC data')
r = requests.post(api, json = data)
print(r)
print(r.content)