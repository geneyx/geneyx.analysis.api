##Patients
The patients API is used to retrieve the list of patients in the account

#URL: 
https://analysis.geneyx.com/api/patients

#China Domain:
https://fa.shanyint.com/api/SampleAssignment

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
        " DNA23644",
        " DNA23645",
        " WGS-23656",
        "01",
        "10000",
        "11111",
        "123",
        "1-2-phenotypes-test-chineese",
        "13671",
        "14082",
        "14082_valid",
        "14082-yaara",
        "14083",
        "15041976",
        "18535",
        "1-88200246",
        "22NR00308",
        "22NR00328",
        "23656-restored-test-for-v5.0",
        "33333",
        "34862",
        "34864",
        "34864_S81",
        "34920",
        "34920_S13",
        "35397",
        "35397_S16",
        "44444",
        "45454",
        "5.0-benchmarking-62436756",
        "5.0-benchmarking-I_17159",
        "5.0-benchmarking-I_17160",
        "5.0-benchmarking-I_17161",
        "5.6",
        "5.9",
        "55555",
        "623",
        "62342",
        "62436756",
        "62531183",
        "66666",
        "68349",
        "68349_test",
        "68349-1000000-lines",
        "77777",
        "88888",
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}