##Samples
The samples API is used to retrieve the list of samples in the account.

#Request URL:
https://analysis.geneyx.com/api/Samples

#China Domain:
https://fa.shanyint.com/api/Samples

#Action: 
POST

#Payload: 
JSON structure 

#Category    Parameter		Description          Required
Auth        ApiUserId       The API user Id      Yes
            ApiUserKey      The API user key     Yes
			
#Example
{
  "ApiUserId": "enter api user ID",
  "ApiUserKey": "enter api user key"
}

#Response
{
    "Code": "success",
    "Data": [
        "Example3"
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}