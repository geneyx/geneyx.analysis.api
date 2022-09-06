##BatchSeqSamples
The batch seq samples API is used for retrieving the sequencing samples performed in batch from account. 

#URL:
https://analysis.geneyx.com/api/BatchSeqSamples

#China Domain:
https://fa.shanyint.com/api/BatchSeqSamples

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
            "SerialNumber": "22NR00319",
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
            "Notes": null,
            "Relation": 0,
            "RelationName": "Self",
            "UseConsent": null,
            "CollectionSampleId": null,
            "FastqFilesCount": 2,
            "DataSourceId": "b1b6c264-385b-4553-ad3f-efd359e74871",
            "DataSource": "temp S3",
            "Files": [
                {
                    "ID": "17613ba8-99a0-43a3-9bda-d941598d85e6",
                    "SeqSampleId": "f4de815e-a8cb-44ac-9e82-ab1fb49e9fed",
                    "FileTypeName": "FastQ",
                    "FileType": 1,
                    "FileSubType": 0,
                    "FileName": "22NR00319_S19_R1_001.fastq.gz",
                    "Ordinal": 1,
                    "Status": 10,
                    "StatusName": "Done",
                    "CreateDate": "2022-03-15T16:51:14.693",
                    "FileSize": 3996953686,
                    "DownloadedSize": 3996953686,
                    "Retries": 0,
                    "ErrorMessage": null
                },
                {
                    "ID": "3c97dad8-879e-4c80-9d28-d6215e2ed0eb",
                    "SeqSampleId": "f4de815e-a8cb-44ac-9e82-ab1fb49e9fed",
                    "FileTypeName": "FastQ",
                    "FileType": 1,
                    "FileSubType": 0,
                    "FileName": "22NR00319_S19_R2_001.fastq.gz",
                    "Ordinal": 2,
                    "Status": 10,
                    "StatusName": "Done",
                    "CreateDate": "2022-03-15T16:51:14.693",
                    "FileSize": 4124355894,
                    "DownloadedSize": 4124355894,
                    "Retries": 0,
                    "ErrorMessage": null
                }
            ],
            "ID": "f4de815e-a8cb-44ac-9e82-ab1fb49e9fed",
            "CreatedByUser": "Eli Sward",
            "CreateDate": "2022-03-15T16:47:23.327",
            "ModifiedByUser": "Eli Sward",
            "ModifyDate": "2022-03-15T16:47:23.327"
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}