##GetVcfSampleArtifact
The get vcf sample coverage API is used for retrieving the vcf coverage statistics.  

#URL:
https://analysis.geneyx.com/api/GetVcfSampleCoverage

#China Domain:
https://fa.shanyint.com/api/GetVcfSampleCoverage

#Action:
POST

#Payload:
JSON Structure

#Category    Parameter            		Description     		Required
Auth        ApiUserId            		The API user Id     	Yes
            ApiUserKey           		The API user key    	Yes
Sample		sampleSn					The VCF serial ID		Yes

#Example
{
    "ApiUserKey": "enter api key",
    "ApiUserId": "enter api ID",
    "sampleSn": "Sample3b",
}

#Response 

Returns .gz file with sample coverage