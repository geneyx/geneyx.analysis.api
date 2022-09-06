##Enrichment Kits
The enrichment kit API is used to retrieve the list of enrichment kits in the account

#URL: 
https://analysis.geneyx.com/api/enrichmentKits

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
        "Agilent SureSelect Clinical Research Exome V2",
        "Agilent SureSelect Human All Exon V5",
        "Agilent SureSelect Human All Exon V6 r2",
        "Agilent SureSelect Human All Exon V7",
        "Agilent SureSelect Human All Exon V8",
        "ALL",
        "Default - Exons only",
        "DNAUnlockedV2",
        "genotyping-test",
        "IDT xGen Exome Research Panel v1.0",
        "IDT xGen Exome Research Panel v2.0",
        "Illumina TruSeq Exome Targeted Regions Manifest v1.2",
        "Reduced-twist-hg19-for-testing-clinvar-merge",
        "Twist Human Core Exome",
        "Twist Human Core Exome Plus",
        "Twist Human Core Exome with RefSeq targets"
    ],
    "Info": null,
    "MoreInfo": null,
    "NeedEval": false
}