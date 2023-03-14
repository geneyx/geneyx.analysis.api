#!/usr/bin/env python3
import argparse
import os
import requests
import ntpath
import ga_helperFunctions as funcs


#region Helper functions
# ---------------------------------

def _verifyRequiredFields(data):
    funcs.verifyFieldInData('SubjectId', data)

# --------------------------------
#endregion Helper functions

# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_uploadSample_json.py', description='Uploads a set of vcf files as a sample to Geneyx Analysis (using a json file)')
# the files
parser.add_argument('--snvVcf', help = 'The path to the SNV VCF file', required=True)
parser.add_argument('--svVcf', help = 'The path to the SV VCF file')
parser.add_argument('--cnvVcf', help = 'The path to the CNV  VCF file')

# Clinical-record data Json file
parser.add_argument('--data','-d', help = 'data JSON file', default='templates\sample.json')

parser.add_argument('--config','-c', help = 'configuration file', default='ga.config.yml')

args = parser.parse_args()

#read the config file
config = funcs.loadYamlFile(args.config)
print(config)

# ---------------------------------
# Validation
# ---------------------------------
# check the SNV
if (not os.path.exists(args.snvVcf)):
    raise Exception("The file {} does not exist".format(args.snvVcf))

# check the SV
if (args.svVcf != None and not os.path.exists(args.svVcf)):
    raise Exception("The file {} does not exist".format(args.svVcf))

# check the CNV
if (args.cnvVcf != None and not os.path.exists(args.cnvVcf)):
    raise Exception("The file {} does not exist".format(args.cnvVcf))

# ---------------------------------
# Files preparation
# ---------------------------------
snvVcf = args.snvVcf
svVcf = None
if (args.svVcf != None and args.cnvVcf != None):
    print("provided both SV and CNV file need to combine")
    if (not '.vcf' in args.svVcf):
        raise Exception("SV file does not seem to be a VCF file")
    if (not '.vcf' in args.cnvVcf):
        raise Exception("CNV file does not seem to be a VCF file")

    combinedFile = args.svVcf.split('.vcf')[0]+'.combined.vcf'
    print('Combined file is '+combinedFile)
    # save the header 
    cmd = 'zcat -f {} | grep "^#" > {}'.format(args.svVcf, combinedFile)
    os.system(cmd)
    # append the SV
    cmd = 'zcat -f {} | grep -v "^#" >> {}'.format(args.svVcf, combinedFile)
    os.system(cmd)
    # append the CNV
    cmd = 'zcat -f {} | grep -v "^#" >> {}'.format(args.cnvVcf, combinedFile)
    os.system(cmd)

    svVcf = combinedFile

elif(args.svVcf != None):
    print("provided SV file")
    svVcf = args.svVcf
elif(args.cnvVcf != None):
    print("provided CNV file")
    svVcf = args.cnvVcf

# prepare the base names
snvBaseName = None
if (snvVcf != None):
    snvBaseName = ntpath.basename(snvVcf)
svBaseName = None
if (svVcf != None):
    svBaseName = ntpath.basename(svVcf)

#prepare the data to send
data = funcs.loadDataJson(args.data)
_verifyRequiredFields(data)
if ((not ('SampleSerialNumber' in data)) or data['SampleSerialNumber'] == None):
    data['SampleSerialNumber'] = ntpath.basename(args.snvVcf)
data['SnvFile'] = snvBaseName
data['StructFile'] = svBaseName
# add user connection fields
data['ApiUserKey'] = config['apiUserKey']
data['ApiUserID'] = config['apiUserId']
print(data)


files = { 'snvFile': open(snvVcf, "rb") }
if (svVcf != None):
    files['svFile'] = open(svVcf, "rb")
api = config['server']+'/api/CreateSample'
print('Uploading sample(s)')
r = requests.post(api, json = data, files = files)
print(r)
print(r.content)
