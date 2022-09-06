##GetVcfSampleArtifact
The get vcf sample artifact API is used for retrieving the vcf artifact file for a sample.  

#URL:
https://analysis.geneyx.com/api/GetVcfSampleArtifact

#China Domain:
https://fa.shanyint.com/api/GetVcfSampleArtifact

#Action:
POST

#Payload:
JSON Structure

#Category    Parameter            		Description     		Required
Auth        ApiUserId            		The API user Id     	Yes
            ApiUserKey           		The API user key    	Yes
Sample		sampleSn					The sample serial ID	Yes
			pipelineType				Snv or Cnv				Yes

#Example
{
    "ApiUserKey": "enter api key",
    "ApiUserId": "enter api ID",
    "sampleSn": "Sample3b",
    "pipelineType":"Snv"
}

#Response 
Download 11458aff.vcf_32_artifacts.zip