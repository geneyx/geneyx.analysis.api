##GetVcfSampleArtifact
The get vcf sample qc data API is used for retrieving the vcf qc statistics.  

#URL:
https://analysis.geneyx.com/api/GetVcfSampleQcData

#China Domain:
https://fa.shanyint.com/api/GetVcfSampleQcData

#Action:
POST

#Payload:
JSON Structure

#Category    Parameter            		Description     		Required
Auth        ApiUserId            		The API user Id     	Yes
            ApiUserKey           		The API user key    	Yes
Sample		sampleSn					The vcf serial ID		Yes

#Example
{
    "ApiUserKey": "enter api key",
    "ApiUserId": "enter api ID",
    "sampleSn": "Sample3b",
}

#Response 
{
    "Code": "success",
    "Data": {
        "ID": "a5cc8bc9-8533-4823-961d-ad0449fdf679",
        "PassedReadsNum": 28383320,
        "FailedReadsNum": 0,
        "MappedReadsNum": 28348040,
        "PairedReadsNum": 28383320,
        "MeanCoverage": 61.54,
        "Percent5x": 95.84,
        "Percent20x": 90.78,
        "Percent50x": 60.3,
        "BedFilePosNum": 38098418,
        "AvrAlignCoverage": 23667627.0,
        "AlignedReads": 23667627
    },
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}