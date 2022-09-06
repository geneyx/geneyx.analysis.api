##Protocols
The sequence machine API is used to retrieve the list of protocols in the account

#URL: 

https://analysis.geneyx.com/api/ReportUrl?fileName=xxx

#China Domain:
https://fa.shanyint.com/api/ReportUrl?fileName=xxx

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
            "SerialNumber": "RG_SINGLE",
            "Name": "Single Sample Analysis"
        },
        {
            "SerialNumber": "RG_TRIO",
            "Name": "Trio Analysis"
        },
        {
            "SerialNumber": "TUM_SINGLE",
            "Name": "Tumor Only Analysis"
        },
        {
            "SerialNumber": "TUM_WITH_GERMLINE",
            "Name": "Tumor / Normal Analysis"
        },
        {
            "SerialNumber": "RG_SNV_SV",
            "Name": "Single Sample SNV/SV"
        },
        {
            "SerialNumber": "SCR_CARRIER",
            "Name": "Carrier Screening"
        },
        {
            "SerialNumber": "SCR_CANCER",
            "Name": "Cancer Screening"
        },
        {
            "SerialNumber": "RG_MITO",
            "Name": "Mitochondria Analysis"
        },
        {
            "SerialNumber": "RG_CNV",
            "Name": "Germline - SV"
        }
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}
			