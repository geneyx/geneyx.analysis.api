#!/usr/bin/env python3
import argparse
import os
import requests
import ga_helperFunctions as funcs


# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_uploadBatch.py', description='Uploads and executes a sample batch file to Geneyx Analysis')
parser.add_argument('--batchFile', help = 'The path to the batch file (defined by GA template)', required=True)
parser.add_argument('--config','-c', help = 'configuration file', default='ga.config.yml')

args = parser.parse_args()

#read the config file
config = funcs.loadYamlFile(args.config)

# ---------------------------------
# Validation
# ---------------------------------
# check the batchFile
if (not os.path.exists(args.batchFile)):
    raise Exception("The file {} does not exist".format(args.batchFile))


batchFile = args.batchFile

print(config)

#prepare the data to send
data = {
			'ApiUserKey': config['apiUserKey'],
			'ApiUserID': config['apiUserId']
	    }

files = { 'batchFile': open(batchFile, "rb") }

api = config['server']+'/api/CreateBatch'
print('Uploading batch')
print(api)
print(data)
r = requests.post(api, data = data, files = files)
print(r)
print(r.content)