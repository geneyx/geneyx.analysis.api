##Sequence Machines
The sequence machine API is used to retrieve the list of 
sequence machines in the account.

#Request URL:
https://analysis.geneyx.com/api/SequenceMachines

#China Domain:
https://fa.shanyint.com/api/SequenceMachines

#Action: 
POST

#Payload: 
JSON structure 

#Category    Parameter		Description          Required
Auth        ApiUserId       The API user Id      Yes
            ApiUserKey      The API user key     Yes
			
#Example:
{
  "ApiUserId": "enter api user ID",
  "ApiUserKey": "enter api user key"
}

#Response
{
    "Code": "success",
    "Data": [
        "HiSeq 2500",
        "HiSeq 4000",
        "Ion GeneStudio S5",
        "Ion Torrent Genexus",
        "iSeq",
        "MiniSeq",
        "MiSeq",
        "MiSeq DX",
        "NextSeq 1000",
        "NextSeq 2000",
        "NextSeq 500",
        "NextSeq 550",
        "NextSeq DX 550",
        "NovaSeq 6000"
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}