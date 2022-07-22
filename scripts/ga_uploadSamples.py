#!/usr/bin/env python3
import argparse
import yaml
import os
import sys
import requests
import json
import datetime
import ntpath

# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_uploadSamples.py', description='Uploads a set of vcf files as a sample to Geneyx Analysis')
# the files
parser.add_argument('--snvVcf', help = 'The path to the SNV VCF file', required=True)
parser.add_argument('--svVcf', help = 'The path to the SV VCF file')
parser.add_argument('--cnvVcf', help = 'The path to the CNV  VCF file')

# sample data
parser.add_argument('--sampleId', help = 'The sample id (serial number)')
parser.add_argument('--sampleTakenDate', help = 'Sample taken date')
parser.add_argument('--sampleSequenceDate', help = 'Sample sequence date')
parser.add_argument('--sampleReceiveDate', help = 'Sample receive date')
parser.add_argument('--sampleType', help = 'Sample type', choices=['RnaSeq','DnaSeq'], default='DnaSeq')
parser.add_argument('--sampleTarget', help = 'Sample target', choices=['WholeGenome','Exome','GenePanel','TargetRegion','ClinicalExome'], default='Exome')
parser.add_argument('--sampleSource', help = 'Sample source', choices=['GermLine','Tumor','Blood','Buccal','Mitochondria','Saliva'], default='GermLine')
parser.add_argument('--seqMachineId', help = 'The sequence machine id - From sequence machines listed in the account')
parser.add_argument('--kitId', help = 'The enrichment kit id (bed file) - From enrichment kits listed in the account')
parser.add_argument('--genomeBuild', help = 'The genome build of this sample', choices=['hg19','hg38'], default='hg19')
parser.add_argument('--sampleNotes', help = 'Sample notes')
parser.add_argument('--sampleQcData', help = 'Sample QC data as json string')

parser.add_argument('--sampleRelation', help = 'Sample relation', choices=['Self','Mother','Father','Sibling','Twin','MotherRelative','FatherRelative','Other'], default='Self')

# sample external files
parser.add_argument('--bamUrl', help = 'Url of the FASTQ file')

#patient data
parser.add_argument('--patientId', help = 'patient id (serial number)', required=True)
parser.add_argument('--patientName', help = 'patient name')
parser.add_argument('--patientGender', help = 'patient gender', choices=['F','M',''], default='')
parser.add_argument('--patientDateOfBirth', help = 'patient date of birth')
parser.add_argument('--patientConsanguinity', help = 'patient consanguinity')
parser.add_argument('--patientPopulationType', help = 'patient population type')
parser.add_argument('--patientPaternalAncestry', help = 'patient parental ancenstry')
parser.add_argument('--patientMaternalAncestry', help = 'patient maternal ancestry')
parser.add_argument('--patientFamilyHistory', help = 'patient family history')
parser.add_argument('--patientHasBioSample', help = 'patient indicate that a bio sample exists')
parser.add_argument('--patientUseConsentPersonal', help = 'patient have personal use consent')
parser.add_argument('--patientUseConsentClinical', help = 'patient have clinical use consent')

parser.add_argument('--groupAssignmentCode', help = 'the group assignment code - for sample assignment')
parser.add_argument('--groupAssignmentName', help = 'the group assignment name - for sample assignment')

# commands (optional)
parser.add_argument('--skipAnnotation', help = 'skip performingannotation after upload', action="store_true")
parser.add_argument('--config','-c', help = 'configuration file', default='ga.config.yml')

# ---------------------------------
# Helper functions
# ---------------------------------
def _loadYamlFile(file):
    with open(file, 'r') as stream:
        try:
            obj = yaml.load(stream)
            return obj
        except yaml.YAMLError as exc:
            print(exc)


args = parser.parse_args()
#read the config file
config = _loadYamlFile(args.config)

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
			'ApiUserKey': config['apiUserKey'],
			'ApiUserID': config['apiUserId'],
			'SampleSerialNumber': sampleId,
			'SampleSequenceDate': args.sampleSequenceDate,
            'SampleTakenDate': args.sampleTakenDate,
            'SampleReceivedDate': args.sampleReceiveDate,
            'SampleType': args.sampleType,
            'SampleTarget': args.sampleTarget,
            'SampleSource': args.sampleSource,
            'SampleSequenceMachineId': args.seqMachineId,
            'SampleEnrichmentKitId': args.kitId,
            'SampleGenomeBuild': args.genomeBuild,
            'SampleNotes': args.sampleNotes,
            'SampleRelation': args.sampleRelation,
            'sampleQcData': args.sampleQcData,
            'sampleQcData': args.sampleQcData,
            'bamUrl': args.bamUrl,
            'SnvFile': snvBaseName,
            'StructFile': svBaseName,
            'SubjectId': args.patientId,
            'SubjectName': args.patientName,
            'SubjectGender': args.patientGender,
            'SubjectDateOfBirth': args.patientDateOfBirth,
            'SubjectConsanguinity': args.patientConsanguinity,
            'SubjectPopulationType': args.patientPopulationType,
            'SubjectPaternalAncestry': args.patientPaternalAncestry,
            'SubjectMaternalAncestry': args.patientMaternalAncestry,
            'SubjectFamilyHistory': args.patientFamilyHistory,
            'SubjectHasBioSample': args.patientHasBioSample,
            'SubjectUseConsentPersonal': args.patientUseConsentPersonal,
            'SubjectUseConsentClinical': args.patientUseConsentClinical,
            'SkipAnnotation': args.skipAnnotation
	    }

# Handle group assignment		
if args.groupAssignmentCode != None and args.groupAssignmentName != None:
	data['GroupAssignment'] = [{ 'Code':args.groupAssignmentCode, 'Name': args.groupAssignmentName}]

files = { 'snvFile': open(snvVcf, "rb") }
if (svVcf != None):
    files['svFile'] = open(svVcf, "rb")
api = config['server']+'/api/CreateSample'
print('Uploading sample(s)')
r = requests.post(api, data = data, files = files)
print(r)
print(r.content)
