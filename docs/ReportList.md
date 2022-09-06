##Report List
The report list api is used to get new reports created on the account from a given date.

#URL:
https://analysis.geneyx.com/api/ReportList?startTime=xxx
	
#China Domain:
https://fa.shanyint.com/api/ReportUrl?fileName=xxx

#Action: 
	POST
#Payload: 
	JSON Structure
	
#Category    Parameter		Description              									Required
Auth        ApiUserId       The API user Id              								Yes
            ApiUserKey      The API user key             								Yes
URL			startTime		The start time of reports retrieval. Format is yyyy/mm/dd	Yes

#Example

{
  "startTime": "2022/08/18",
  "ApiUserId": "Enter API User ID",
  "ApiUserKey": "Enter API User Key"
}

#Response
{
    "Code": "success",
    "Data": [
        {
            "ID": "c3673da0-77fc-4bbc-a869-68cfe19ed21e",
            "ReportFileUrl": "II220818112106 - Single Sample Analysis - 220818_1722.pdf",
            "DataFileUrl": "II220818112106 - Single Sample Analysis - 220818_1722 - data.xlsx",
            "Summary": null,
            "CreatedByUser": "Eli Sward",
            "CreateDate": "2022-08-18T17:22:33.783",
            "PatientSn": "ExampleImporta",
            "PatientName": "Example12",
            "CaseSn": "II220818112106",
            "CaseName": "Single Sample Analysis",
            "SampleSn": "Example3",
            "SampleVcfUrl": "GeneyxEval.vcf.gz"
        }
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}