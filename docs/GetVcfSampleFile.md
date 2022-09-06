##GetVcfSampleArtifact
The get vcf sample file API is used for retrieving the vcf file for the sample.  

#URL:
https://analysis.geneyx.com/api/GetVcfSampleFile

#China Domain:
https://fa.shanyint.com/api/GetVcfSampleFile

#Action:
POST

#Payload:
JSON Structure

#Category    Parameter            		Description     		Required
Auth        ApiUserId            		The API user Id     	Yes
            ApiUserKey           		The API user key    	Yes
Sample		sampleSn					The sample serial ID	Yes
			fileType					Snv or Sv				Yes

#Example
{
    "ApiUserKey": "enter api key",
    "ApiUserId": "enter api ID",
	"fileType": "Snv",
    "sampleSn": "Sample3b",
}

#Response 

Returns requested file: sample3b.vcf.gz

