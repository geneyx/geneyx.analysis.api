import json
import yaml

def loadYamlFile(file):
    with open(file, 'r') as stream:
        try:
            obj = yaml.safe_load(stream)
            return obj
        except yaml.YAMLError as exc:
            print(exc)

def loadDataJson(file):
    print(file)
    with open(file, 'r') as stream:
        try:
            data = json.load(stream)            
            return data
        except KeyError as exc:
            print(exc)

def verifyFieldInData(fieldName: str, data):
    if ((not ('fieldName' in data)) or data['fieldName'] == None):
        raise Exception(f'No "{fieldName}" field in data json file, but defined as required. Please fix data file.')