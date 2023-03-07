import argparse
import requests
import json
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

#region Helper functions
# ---------------------------------
def _loadYamlFile(file):
    with open(file, 'r') as stream:
        try:
            obj = yaml.load(stream, Loader=Loader)
            return obj
        except yaml.YAMLError as exc:
            print(exc)

def _loadDataJson(file):
    print(file)
    with open(file, 'r') as stream:
        try:
            data = json.load(stream)            
            return data
        except KeyError as exc:
            print(exc)

def _verifyRequiredFields(data):
    #TODO: check if exists
    if ((not ('ProtocolId' in data)) or data['ProtocolId'] == None):
        raise Exception('No "ProtocolId" field in data json file, but defined as required. Please fix data file.')
    if ((not ('SubjectId' in data)) or data['SubjectId'] == None):
        raise Exception('No "SubjectId" field in data json file, but defined as required. Please fix data file.')
    if ((not ('ProbandSampleId' in data)) or data['ProbandSampleId'] == None):
        raise Exception('No "ProbandSampleId" field in data json file, but defined as required. Please fix data file.')

# --------------------------------
#endregion Helper functions


# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_uploadCase.py', description='Uploads a case to Geneyx Analysis')

# Case data Json file
parser.add_argument('--data','-d', help = 'data JSON file', required=True, default='createCase.json')

# commands (optional)
parser.add_argument('--config','-c', help = 'configuration file', default='ga.config.yml')

args = parser.parse_args()
#read the config file
config = _loadYamlFile(args.config)

print(config)

#prepare the data to send
data = _loadDataJson(args.data)
_verifyRequiredFields(data)

print(data)

# add user connection fields
data['ApiUserKey'] = config['apiUserKey']
data['ApiUserID'] = config['apiUserId']

# send request
api = config['server']+'/api/CreateCase'
print('Creating case')
r = requests.post(api, json = data)
print(r)
print(r.content)