##Data Entry Batches
The data entry api is used to retrieve the list of batches performed in an account. 

#URL: 
<domain>/api/DataEntryBatches

#URL:
https://analysis.geneyx.com/api/DataEntryBatches

#China Domain:
https://fa.shanyint.com/api/DataEntryBatches

#Action: 
POST

#Payload: 
JSON structure 

#Category    Parameter		Description          Required
Auth        ApiUserId       The API user Id      Yes
            ApiUserKey      The API user key     Yes
			

#Example
{
  "ApiUserId": "enter api user id",
  "ApiUserKey": "enter api user key"
}
			
#Response
{
    "Code": "success",
    "Data": [
        {
            "FileName": "BatchImportTemplate(Geneyx).txt",
            "ErrorResult": null,
            "Status": 2,
            "StatusName": "Done",
            "Name": "BatchImportTemplate(Geneyx).txt-20220315-164722",
            "ID": "a75853f8-cb81-420f-a0f3-81fecb2d8b12",
            "CreatedByUser": "Eli Sward",
            "CreateDate": "2022-03-15T16:47:25.157",
            "ModifiedByUser": "Eli Sward",
            "ModifyDate": "2022-03-15T16:47:25.157"
        },
        {
            "FileName": "batch-second-run-96-exomes-29-03-22.txt",
            "ErrorResult": null,
            "Status": 1,
            "StatusName": "Processing",
            "Name": "batch-second-run-96-exomes-29-03-22.txt-20220329-085840",
            "ID": "f717912a-31ff-4fe4-bfdf-d19ad96dbd6f",
            "CreatedByUser": "Yaara Unger",
            "CreateDate": "2022-03-29T08:58:43.557",
            "ModifiedByUser": "Yaara Unger",
            "ModifyDate": "2022-03-29T08:58:43.557"
        },
        {
            "FileName": "batch-second-run-no-cnv-96-exomes-29-03-22.txt",
            "ErrorResult": null,
            "Status": 2,
            "StatusName": "Done",
            "Name": "batch-second-run-no-cnv-96-exomes-29-03-22.txt-20220329-143234",
            "ID": "447d4bcc-f4cd-40cb-9c5e-5d7a5d33fffb",
            "CreatedByUser": "Yaara Unger",
            "CreateDate": "2022-03-29T14:32:35.01",
            "ModifiedByUser": "Yaara Unger",
            "ModifyDate": "2022-03-29T14:32:35.01"
        }
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}