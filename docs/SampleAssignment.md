##Sample Permission
The sample assignment API is used for updating the permissions for users within a group for given samples.

#URL:
https://analysis.geneyx.com/api/SampleAssignment

#China Domain:
https://fa.shanyint.com/api/SampleAssignment

#Action:
Post
#Payload:
JSON Structure

#Category    Parameter            		Description              											Required
Auth        ApiUserId            		The API user Id              										Yes
            ApiUserKey           		The API user key             										Yes
Sample		SerialNumber				The sample Serial Number of the VCF samples.        				Yes
Assignment	GroupAssignment				List of groups the sample is assigned to, each has: Code, Name. 	No
			
#Example
{
  "SerialNumber":"Sample3b",
  "GroupAssignment": [
	{
		"Code": "Cardio",
		"Name": "Cardio",
    }
	],
  "ApiUserId": "enter API id",
  "ApiUserKey": "enter API key"
}


#Response
{
    "Code": "success",
    "Data": {
        "UserId": null,
        "FullName": null,
        "Name": null,
        "Email": null,
        "AssignedBy": "Eli Sward",
        "AssignDate": "2022-08-24T12:58:24.2372339Z",
        "GroupCodes": [
            "Cardio"
        ],
        "Groups": [
            {
                "Code": "Cardio",
                "Name": "Cardio"
            }
        ]
    },
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}