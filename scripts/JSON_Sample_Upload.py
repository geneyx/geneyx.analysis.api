#!/usr/bin/env python3
import argparse
import os
import requests
import ntpath
import ga_helperFunctions as funcs
import json

# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(prog='ga_uploadSample.py', description='Uploads a set of vcf files as a sample to Geneyx Analysis')
# path to the JSON file containing sample information
parser.add_argument('--jsonFile', help='Path to the JSON file containing sample information', required=True)
parser.add_argument('--config','-c', help='Configuration file', default='ga.config.yml')
args = parser.parse_args()

# Read the config file
config = funcs.loadYamlFile(args.config)

# Function to process each sample
def process_sample(sample):
    snvVcf = sample['snvVcf']
    svVcf = sample['svVcf'] if 'svVcf' in sample else None
    cnvVcf = sample['cnvVcf'] if 'cnvVcf' in sample else None
    genomeBuild = sample.get('genomeBuild', 'hg19')
    patientId = sample['patientId']

    if not os.path.exists(snvVcf):
        raise Exception("The file {} does not exist".format(snvVcf))
    
    if svVcf and not os.path.exists(svVcf):
        raise Exception("The file {} does not exist".format(svVcf))
    
    if cnvVcf and not os.path.exists(cnvVcf):
        raise Exception("The file {} does not exist".format(cnvVcf))
    
    # Combine SV and CNV files if both are provided
    combinedVcf = None
    if svVcf and cnvVcf:
        combinedFile = svVcf.split('.vcf')[0] + '.combined.vcf'
        print('Combining SV and CNV files into {}'.format(combinedFile))
        os.system(f'zcat -f {svVcf} | grep "^#" > {combinedFile}')
        os.system(f'zcat -f {svVcf} | grep -v "^#" >> {combinedFile}')
        os.system(f'zcat -f {cnvVcf} | grep -v "^#" >> {combinedFile}')
        svVcf = combinedFile
    
    # Prepare the sample data
    sampleId = sample['patientId'] 
    snvBaseName = ntpath.basename(snvVcf)
    svBaseName = ntpath.basename(svVcf) if svVcf else None
    
    data = {
        'ApiUserKey': config['apiUserKey'],
        'ApiUserID': config['apiUserId'],
        'CustomerAccountKey': sample.get('customerAccountKey', ''),
        'SampleSerialNumber': sampleId,
        'SampleSequenceDate': sample.get('sampleSequenceDate', ''),
        'SampleTakenDate': sample.get('sampleTakenDate', ''),
        'SampleReceivedDate': sample.get('sampleReceiveDate', ''),
        'SampleType': sample.get('sampleType', 'DnaSeq'),
        'SampleTarget': sample.get('sampleTarget', 'Exome'),
        'SampleSource': sample.get('sampleSource', 'GermLine'),
        'SampleSequenceMachineId': sample.get('seqMachineId', ''),
        'SampleEnrichmentKitId': sample.get('kitId', ''),
        'SampleGenomeBuild': genomeBuild,
        'SampleNotes': sample.get('sampleNotes', ''),
        'SampleRelation': sample.get('sampleRelation', 'Self'),            
        'sampleQcData': sample.get('sampleQcData', ''),            
        'ExcludeFromLAF': sample.get('excludeFromLAF', False),
        'bamUrl': sample.get('bamUrl', ''),
        'methylationUrl': sample.get('methylationUrl', ''),            
        'SnvFile': snvBaseName,
        'StructFile': svBaseName,
        'SubjectId': patientId,
        'SubjectName': sample.get('patientName', ''),
        'SubjectGender': sample.get('patientGender', ''),
        'SubjectDateOfBirth': sample.get('patientDateOfBirth', ''),
        'SubjectConsanguinity': sample.get('patientConsanguinity', ''),
        'SubjectPopulationType': sample.get('patientPopulationType', ''),
        'SubjectPaternalAncestry': sample.get('patientPaternalAncestry', ''),
        'SubjectMaternalAncestry': sample.get('patientMaternalAncestry', ''),
        'SubjectFamilyHistory': sample.get('patientFamilyHistory', ''),
        'SubjectHasBioSample': sample.get('patientHasBioSample', ''),
        'SubjectUseConsentPersonal': sample.get('patientUseConsentPersonal', ''),
        'SubjectUseConsentClinical': sample.get('patientUseConsentClinical', ''),
        'SkipAnnotation': sample.get('skipAnnotation', False)
    }

    # Handle group assignment
    if sample.get('groupAssignmentCode') and sample.get('groupAssignmentName'):
        data['GroupAssignment'] = [{'Code': sample['groupAssignmentCode'], 'Name': sample['groupAssignmentName']}]
    
    files = {'snvFile': open(snvVcf, "rb")}
    if svVcf:
        files['svFile'] = open(svVcf, "rb")
    
    api = config['server'] + '/api/CreateSample'
    print('Uploading sample {}'.format(sampleId))
    r = requests.post(api, data=data, files=files)
    print(r)
    print(r.content)

# Read the JSON file
with open(args.jsonFile, 'r') as f:
    samples = json.load(f)['samples']

# Process each sample in the JSON file
for sample in samples:
    process_sample(sample)
