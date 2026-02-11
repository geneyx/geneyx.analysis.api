import argparse
import requests
import json
import ga_helperFunctions as funcs

def _verifyRequiredFields(data):
    funcs.verifyFieldInData('CaseSn', data)
    funcs.verifyFieldInData('AssociatedSamples', data)

def _validateAssociatedSamples(associated_samples):
    if not isinstance(associated_samples, list):
        raise ValueError("AssociatedSamples must be a list")
    for sample in associated_samples:
        if 'SampleId' not in sample:
            raise ValueError("Each associated sample must have a 'SampleId' field")
        if 'Relation' not in sample:
            raise ValueError("Each associated sample must have a 'Relation' field")
        if sample['Relation'] not in ['Mother', 'Father', 'Self','Sibling','Twin','MotherRelative','FatherRelative','Other']:
            raise ValueError("Relation field must be one of 'Mother', 'Father', 'Self', 'Sibling', 'Twin', 'MotherRelative', 'FatherRelative' or 'Other'")
        if 'Affected' not in sample:
            raise ValueError("Each associated sample must have an 'Affected' field")
        if sample['Affected'] not in ['Affected', 'Unaffected','Mixed', 'Unknown']:
            raise ValueError("Affected field must be one of 'Affected', 'Unaffected', 'Mixed' or 'Unknown'")

parser = argparse.ArgumentParser(prog='ga_setCaseAssociatedSamples.py', description='Associate samples with an existing case in Geneyx Analysis')
parser.add_argument('--caseSn', required=True, help='The case serial number')
parser.add_argument('--associatedSamples', required=True, help='JSON string or path to JSON file with associated samples')
parser.add_argument('--config','-c', help = 'configuration file', default='ga.config.yml')
args = parser.parse_args()
#prepare the data to send
data = funcs.loadDataJson(args.data)
if data is None:
    raise ValueError("Failed to load data from --data argument")

# Parse associated samples
if args.associatedSamples.endswith('.json'):
    with open(args.associatedSamples, 'r') as f:
        associated_samples = json.load(f)
else:
    associated_samples = json.loads(args.associatedSamples)
_validateAssociatedSamples(associated_samples)
data['AssociatedSamples'] = associated_samples
_verifyRequiredFields(data)


#read the config file
config = funcs.loadYamlFile(args.config)
if config is None:
    raise ValueError(f"Failed to load config file: {args.config}")
print(config)
data['ApiUserKey'] = config['apiUserKey']
data['ApiUserID'] = config['apiUserId']
print(data)

data = {
    "CaseSn": args.caseSn,
    "AssociatedSamples": associated_samples,
    "ApiUserKey": config['apiUserKey'],
    "ApiUserID": config['apiUserId'],
    "CustomerAccountKey": config['customerAccountKey']
}

url = config['server'].rstrip('/') + '/api/setCaseAssociatedSamples'
headers = {'Content-Type': 'application/json'}

print(f"Sending POST to {url} with data:")
print(json.dumps(data, indent=2))

response = requests.post(url, json=data, headers=headers)
print("Status code:", response.status_code)
print("Response:", response.text)
