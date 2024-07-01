#!/usr/bin/env python3
import argparse
import os
import requests
import ntpath
import ga_helperFunctions as funcs


# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_uploadFilesToSample.py', description='Uploads a SNV and SV  files to existing sample')
# the files
parser.add_argument('--snvVcf', help = 'The path to the SNV VCF file')
parser.add_argument('--svVcf', help = 'The path to the SV VCF file')


# sample data
parser.add_argument('--sampleId', help = 'The sample id (serial number)', required=True)

# commands (optional)
parser.add_argument('--skipAnnotation', help = 'skip performingannotation after upload', action="store_true")
parser.add_argument('--config','-c', help = 'configuration file', default='ga.config.yml')

args = parser.parse_args()

#read the config file
config = funcs.loadYamlFile(args.config)

# ---------------------------------
# Validation
# ---------------------------------
# check the SNV
if (args.snvVcf != None and not os.path.exists(args.snvVcf)):
    raise Exception("The file {} does not exist".format(args.snvVcf))

# check the SV
if (args.svVcf != None and not os.path.exists(args.svVcf)):
    raise Exception("The file {} does not exist".format(args.svVcf))



# ---------------------------------
# Files preparation
# ---------------------------------
snvVcf = args.snvVcf
svVcf = args.svVcf

# ---------------------------------
# prepare the parameters for upload
# ---------------------------------
sampleId = args.sampleId
if (sampleId == None):
    sampleId = ntpath.basename(args.snvVcf)

print(config)

# prepare the base names
snvBaseName = None
if (snvVcf != None):
    snvBaseName = ntpath.basename(snvVcf)
svBaseName = None
if (svVcf != None):
    svBaseName = ntpath.basename(svVcf)

#prepare the data to send
data = {
        'apiUserKey': config['apiUserKey'],
        'apiUserID': config['apiUserId'],
        'sampleSn': sampleId,
        'SnvFile': snvBaseName,
        'SvFile': svBaseName,
        'SkipAnnotation': args.skipAnnotation
    }

files = {}
if (snvVcf != None):
    files['snvFile'] = open(snvVcf, "rb")
if (svVcf != None):
    files['svFile'] = open(svVcf, "rb")
api = config['server']+'/api/uploadFilesToSample'
print('Uploading sample(s)')
r = requests.post(api, data = data, files = files)
print(r)
print(r.content)
