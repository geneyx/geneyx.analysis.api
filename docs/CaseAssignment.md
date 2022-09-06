##Case Assignment

The case assignment API is used for updating the user assignment for a case.

#URL:
<domain>/api/CaseAssignment

#URL:
https://analysis.geneyx.com/api/CaseAssignment

#China Domain:
https://fa.shanyint.com/api/CaseeAssignment

#Action:
POST
#Payload:
JSON Structure

#Category    Parameter            		Description              																					Required
Auth        ApiUserId            		The API user Id              																				Yes
            ApiUserKey           		The API user key             																				Yes
Case		SerialNumber		   		Serial number of the analysis.																				Yes 
Assignment	UserId						The user Id the case is assigned to. 																		No
			FullName					The full name of the user the case is assigned to. 															No
			
#Example
{
  "SerialNumber":"G-Q200827162733",
  "AssignedToUserId": "00000000-0000-0000-0000-000000000000",
  "AssignedToFullName": "Raviv Itzhaky",
  "ApiUserId": "enter user api id",
  "ApiUserKey": "enter user api key"
}

#Response
{
    "Code": "success",
    "Data": {
        "UserId": "00000000-0000-0000-0000-000000000000",
        "FullName": "Raviv Itzhaky",
        "AssignedBy": "Eli Sward",
        "AssignDate": "2022-08-24T17:30:43.6329522Z",
        "Name": "Raviv Itzhaky",
        "Email": ""
    },
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}
			