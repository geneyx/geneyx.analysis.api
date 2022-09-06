##BatchVcfSamples
The batch vcf samples API is used for retrieving the vcf samples from a batch run within the account. 

#URL:
https://analysis.geneyx.com/api/BatchVcfSamples

#China Domain:
https://fa.shanyint.com/api/BatchVcfSamples

#Action:
POST

#Payload:
JSON Structure

#Category    Parameter            		Description     	Required
Auth        ApiUserId            		The API user Id     Yes
            ApiUserKey           		The API user key    Yes
Case		batchName					The batch name		Yes

#Example
{
  "batchName": "batch-second-run-no-cnv-96-exomes-29-03-22.txt-20220329-143234",
  "ApiUserId": "enter api user id",
  "ApiUserKey": "enter api user key"
}

#Response
{
    "Code": "success",
    "Data": [
        {
            "PatientId": "49c02bc2-02c6-4fa4-ae3c-5563b6d598fd",
            "Patient": "22NR00319",
            "SerialNumber": "22NR00319.dragen.wes.hg38.20220329-143236",
            "SequenceMachineId": null,
            "SequenceMachine": null,
            "EnrichmentKitId": "df7573e6-b4d4-40e9-bd54-5fc2554ca408",
            "EnrichmentKit": "Geneyx Target Region and genotyping MAR-29-2022",
            "EnrichmentKitDescription": "Geneyx Target Region and genotyping MAR-29-2022",
            "TakenDate": null,
            "SeqDate": null,
            "ReceivedDate": null,
            "StatusName": null,
            "Type": null,
            "TypeName": null,
            "Target": 2,
            "TargetName": "Exome",
            "Source": null,
            "SourceName": null,
            "BamUrl": "https://analysis.geneyx.com/api/gdbam?bamfile=f27b399d-bd30-4dc1-b028-b5a3dcc1d1a6/22NR00319.dragen.wes.hg38.20220329-143236.bam",
            "BamFileExists": true,
            "ErrorDescription": null,
            "Notes": null,
            "QcData": null,
            "SeqQcData": null,
            "Relation": 0,
            "RelationName": "Self",
            "GenomeBuild": 1,
            "GenomeBuildName": "hg38",
            "SeqSampleId": "f4de815e-a8cb-44ac-9e82-ab1fb49e9fed",
            "Assignment": {
                "UserId": null,
                "FullName": null,
                "Name": null,
                "Email": null,
                "AssignedBy": null,
                "AssignDate": "0001-01-01T00:00:00",
                "GroupCodes": [],
                "Groups": []
            },
            "Files": [
                {
                    "ID": "1d47faef-424a-459f-881c-ae4213f4ceda",
                    "FileTypeName": "BAM",
                    "FileType": 40,
                    "FileSubType": 0,
                    "FileName": "22NR00319.dragen.wes.hg38.20220329-143236.bam",
                    "CreateDate": "2022-03-29T15:04:51.677"
                },
                {
                    "ID": "00d541b8-8dca-4939-ad89-4542359aae23",
                    "FileTypeName": "BAI",
                    "FileType": 41,
                    "FileSubType": 0,
                    "FileName": "22NR00319.dragen.wes.hg38.20220329-143236.bam.bai",
                    "CreateDate": "2022-03-29T15:04:51.677"
                },
                {
                    "ID": "eb3b7e61-63c6-42c7-a6f3-93d9717565b4",
                    "FileTypeName": "SV",
                    "FileType": 21,
                    "FileSubType": 0,
                    "FileName": "22NR00319.dragen.wes.hg38.20220329-143236.sv.unified.vcf.gz",
                    "CreateDate": "2022-03-29T15:04:51.893"
                },
                {
                    "ID": "bdc91e53-c595-4c33-b442-371a6511855f",
                    "FileTypeName": "SNV",
                    "FileType": 1,
                    "FileSubType": 0,
                    "FileName": "22NR00319.dragen.wes.hg38.20220329-143236.vcf.gz",
                    "CreateDate": "2022-03-29T15:04:48.85"
                }
            ],
            "NewFiles": null,
            "ID": "f27b399d-bd30-4dc1-b028-b5a3dcc1d1a6",
            "CreatedByUser": "Eli Sward",
            "CreateDate": "2022-03-29T14:32:36.253",
            "ModifiedByUser": "Eli Sward",
            "ModifyDate": "2022-03-29T14:32:36.253"
        },
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}