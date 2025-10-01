import os
import json
import gzip
import argparse
import requests
import ga_helperFunctions as funcs
import unify_vcf  # assumes unify_vcf.py is in the same directory

def open_file_auto(path):
    return gzip.open(path, 'rt') if path.endswith('.gz') else open(path, 'r')

def merge_sv_cnv(sv_path, cnv_path, output_path):
    with gzip.open(output_path, 'wt') as out:
        for path in [sv_path, cnv_path]:
            with open_file_auto(path) as f:
                for line in f:
                    if not line.startswith('#') or path == sv_path:
                        out.write(line)

def upload_sample(sample, config):
    def safe_path(value):
        return value if isinstance(value, str) and value.strip().lower() not in ["", "nan"] else None

    snv = safe_path(sample.get("snvVcf"))
    sv = safe_path(sample.get("svVcf"))
    cnv = safe_path(sample.get("cnvVcf"))
    repeat = safe_path(sample.get("repeatVcf"))
    roh = safe_path(sample.get("rohFile"))  # optional

    # Unify if repeat is present
    if repeat:
        base = sample["sampleSerialNumber"]
        unified_path = os.path.join(os.path.dirname(snv), f"{base}.unified.vcf")
        unify_vcf.run(
            output_path=unified_path,
            sv_path=sv,
            cnv_path=cnv,
            repeat_path=repeat,
            roh_bed_path=roh,
            skip_svtype=False
        )
        sv = unified_path + ".gz"

    # Continue with your sample upload logic...
    # For example: return funcs.upload_sample(snv, sv, cnv, repeat, sample, config)


    # If both SV and CNV exist and no repeat → merge them
    elif sv and cnv:
        merged_path = sv.replace('.sv.vcf', '.sv.combined.vcf.gz').replace('.vcf.gz', '.combined.vcf.gz')
        merge_sv_cnv(sv, cnv, merged_path)
        sv = merged_path

    # If only CNV present (and no repeat), use CNV directly as the svFile
    elif cnv and not sv:
        sv = cnv

    # If only SV present (and no repeat), use SV directly
    # (already covered by default, but keeping here for clarity)


    files = {'snvFile': open(snv, 'rb')}
    if sv:
        files['svFile'] = open(sv, 'rb')

    data = {
    'ApiUserKey': config['apiUserKey'],
    'ApiUserID': config['apiUserId'],
    'CustomerAccountKey': sample.get('customerAccountKey', ''),
    'SampleSerialNumber': sample['sampleSerialNumber'],
    'SampleTarget': sample.get('sampleTarget', 'Exome'),
    'SampleGenomeBuild': sample.get('genomeBuild', 'hg19'),
    'SnvFile': os.path.basename(snv),
    'StructFile': os.path.basename(sv) if sv else '',
    'SubjectId': sample.get('SubjectId'),
    'SubjectGender': sample.get('patientGender', ''),
    'Phenotypes': sample.get('Phenotypes', ''),

    # NEW sample metadata fields
    'SampleTakenDate': sample.get('sampleTakenDate'),
    'SampleSequenceDate': sample.get('sampleSequenceDate'),
    'SampleReceiveDate': sample.get('sampleReceiveDate'),
    'SampleType': sample.get('sampleType', 'DnaSeq'),
    'SampleSource': sample.get('sampleSource', 'GermLine'),
    'SeqMachineId': sample.get('seqMachineId'),
    'SampleEnrichmentKitId': sample.get('kitId', ''),
    'SampleNotes': sample.get('sampleNotes'),
    'SampleQcData': sample.get('sampleQcData'),
    'SampleAdvAnalysis': sample.get('sampleAdvAnalysis'),
    'ExcludeFromLAF': sample.get('excludeFromLAF'),

    # External file URLs
    'BamUrl': sample.get('bamUrl'),
    'MethylationUrl': sample.get('methylationUrl'),

    # Group assignment
    'GroupAssignmentCode': sample.get('groupAssignmentCode'),
    'GroupAssignmentName': sample.get('groupAssignmentName'),

    # Patient fields
    'SubjectId': sample.get('SubjectId'),
    'SubjectName': sample.get('SubjectName'),
    'SubjectDateOfBirth': sample.get('SubjectDateOfBirth'),
    'SubjectConsanguinity': sample.get('SubjectConsanguinity'),
    'SubjectPopulationType': sample.get('SubjectPopulationType'),
    'SubjectPaternalAncestry': sample.get('SubjectPaternalAncestry'),
    'SubjectMaternalAncestry': sample.get('SubjectMaternalAncestry'),
    'SubjectFamilyHistory': sample.get('SubjectFamilyHistory'),
    'SubjectHasBioSample': sample.get('SubjectHasBioSample'),
    'SubjectUseConsentPersonal': sample.get('SubjectUseConsentPersonal'),
    'SubjectUseConsentClinical': sample.get('SubjectUseConsentClinical'),
    
    # Relationship to proband (e.g., Self, Mother, etc.)
    'Relation': sample.get('sampleRelation', 'Self'),
}

    print(f"Uploading sample {sample['sampleSerialNumber']}")
    r = requests.post(config['server'] + '/api/CreateSample', data=data, files=files)
    print(r)
    try:
        response_data = r.json()
        if response_data.get("Code") != "success":
            print(f"[ERROR] Sample upload failed for {sample['sampleSerialNumber']}: {response_data.get('Info')}")
    except Exception as e:
        print("[ERROR] Could not decode upload response:", str(e))

    print(r.content)
    return sample['sampleSerialNumber']

def create_case_with_family(entry, proband_id, associated_samples, config):
    protocol = entry.get('ProtocolId')
    phenotypes = entry.get('Phenotypes', '')
    
    case_data = {
    'ApiUserKey': config['apiUserKey'],
    'ApiUserID': config['apiUserId'],
    'ProbandSampleId': proband_id,
    'SubjectId': proband_id,
    'ProtocolId': protocol,
    'Phenotypes': phenotypes
    }
    
    if associated_samples:
        case_data['AssociatedSamples'] = [
            {
                'Relation': s.get('Relation'),
                'SampleId': s.get('SampleId'),
                'Affected': s.get('Affected', 'Unaffected')
            } for s in associated_samples
        ]


    print("Creating case...")
    print("Case payload:")
    print(json.dumps(case_data, indent=2))  # helpful for debugging
    
    r = requests.post(config['server'] + '/api/CreateCase', json=case_data)

    try:
        r.raise_for_status()
        res_json = r.json()
        if res_json.get("Code") == "success":
            print(f"[SUCCESS] Case creation succeeded. Protocol used: {protocol}")
        else:
            print("[WARNING] Case API returned but no case was created:")
            print("Response:", res_json)
    except Exception as e:
        print("[FAILURE] Case creation failed:", str(e))
        print("Raw Response:", r.text)



def process_entry(entry, config):
    # Upload associated samples first
    assoc_samples = entry.get('AssociatedSamples', [])
    for assoc in assoc_samples:
        upload_sample({
            **assoc,
            'SubjectId': assoc['SampleId'],
            'sampleSerialNumber': assoc['SampleId'],
            'genomeBuild': entry.get('genomeBuild', 'hg38'),
            'ProtocolId': entry.get('ProtocolId'),
            'Phenotypes': entry.get('Phenotypes', ''),
            'sampleTarget': assoc.get('sampleTarget', 'Exome')
        }, config)

    # Then upload the proband
    sample_id = upload_sample(entry, config)
    
    # ✅ Add this check before creating the case
    if not entry.get('ProtocolId'):
        print("[ERROR] Missing ProtocolId for sample", entry.get('sampleSerialNumber'))
    
    # Only now create the case
    create_case_with_family(entry, sample_id, assoc_samples, config)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', required=True)
    parser.add_argument('--config', default='ga.config.yml')
    args = parser.parse_args()

    config = funcs.loadYamlFile(args.config)
    with open(args.json, 'r') as f:
        data = json.load(f)['entries']
    for entry in data:
        process_entry(entry, config)
