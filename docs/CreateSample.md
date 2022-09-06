##Create Sample
This API call allows a user/integrator to upload a VCF file and create a corresponding Sample
entry in Geneyx Analysis. Other than the VCF file, additional metadata may be included in the
Sample. Optionally, the Sample entry may be associated with an existing Subject entry (by ID).

#Implementation 

To run this code, you will need to navigate to https://github.com/geneyx/geneyx.analysis.api/. 
There is a green icon for Code. Select the icon and click Download Zip. Extract the files, then navigate 
to the script directory. 

The scripts directory contains:

- ga.config.yml
- ga_uploadSample.py
- UnifiedVcf.py

First you will need to modify the ga.config.yml file to reflect your api ID and api key. Once saved you can then define
the parameters which are listed below. The CMD values will be used for the command line. Please see below, command line request, 
which provides an example of the process.

#Request URL:
https://analysis.geneyx.com/api/createSample

#China Domain:
https://fa.shanyint.com/api/createSample

#Category    Parameter            		CMD Values				Description              																					Required
Auth        ApiUserId            		---						The API user Id              																				Yes
            ApiUserKey           		---						The API user key             																				Yes
			CustomerAccountKey   		---						Geneyx Analysis Customer account key (  																	No
Sample		SampleSerialNumber   		sampleId				Sample ID, name given to the VCF file   																	Yes
			SampleSequenceDate   		sampleSequenceDate		Date when sample was sequenced      																		No
			SampleTakenDate      		sampleTakeDate			Date when sample was taken        																			No
			SampleReceivedDate   		sampleRecieveDate		Date when sample was received       																		No
			SampleSequencingMachineID	seqMachineId			ID of Sequencing Machine entry as defined in customer account.  											No
			SampleEnrichmentKitId  		kitId					ID of Enrichment Kit entry as defined in account  															No
            SampleType       	 		sampleType				May be one of the following: RnaSeq , DnaSeq																No
            SampleTarget      			sampleTarget			May be one of the following: WholeGenome, Exome,GenePanel, TargetRegion										No
            SampleSource      			sampleSource			May be one of the following: Germline, Tumor, Blood, Buccal, Fetal, Saliva, Other							No
			SampleGenomeBuild    		genomeBuild				Maybe one of the following: hg19,hg38																		No
            SampleRelation     			sampleRelation			The sample relation, can be: Self, Mother, Father, Sibling, Twin, MotherRelative, FatherRelative, Other		No
            SampleNotes          		sampleNotes				Free text up to 1024 characters      																		No
            SampleQcData            	sampleQcData			JSON structure for QC data        																			No
            SnvFile         			snvBaseName				The name of the SNV file 		 																			No
            StructFile       			svBaseName				The name of the structural variation file  																	No
            BamUrl                		bamUrl					The URL to the BAM file          																			No
Subject  	SubjectId        			patientId				Unique identified for Subject. May be any string. If an existing subject exists. It will be associated.   	Yes
            SubjectName             	patientName				Name of subject                       																		No
            SubjectGender           	patientGender			May be “M” or “F”                     																		No
            SubjectDateOfBirth     		patientDateOfBirth		Date of birth of subject              																		No
            SubjectConsanguinity    	patientConsanguinity	The subject consanguinity, option are Unkown (Default), Consanguineous, Non-Consanguineous          		No
            SubjectPopulationType   	patientPopulationType	Population type                       																		No
            SubjectPaternalAncestry 	patientPaternalAncestry	Paternal ancestry                     																		No
            SubjectMaternalAncestry 	patientMaternalAncestry	Maternal ancestry                     																		No
            SubjectFamilyHistory    	patientFamilyHistory	The family history                    																		No
Assignment  AssignedToUserId        	groupAssignmentCode		The user id the sample is assigned to. 																		No
            AssignedToFullName      	groupAssignmentName		The full name of the user the sample is assigned to.														No
            GroupAssignment         	GroupAssignment			List of groups the sample is assigned to. Each list item has: Code, Name 									No
File        Files                   	snvVcf, svVcf, cnvVcf	Parameter of type File, must be .vcf or .vcf.gz																No

#Request Example

{
--snvVcf "C:\Users\eliws\OneDrive\Desktop\Geneyx\Production\scripts\GeneyxEval.vcf.gz" 
--sampleId New3 
--sampleSequenceDate 01/02/03 
--sampleTakenDate 02/03/04 
--sampleReceiveDate 03/18/22 
--seqMachineId "NextSeq 2000" 
--kitId "Default - Exons only" 
--sampleType DnaSeq 
--sampleTarget Exome 
--sampleSource GermLine 
--genomeBuild hg19 
--sampleNotes DemonstrationImport 
--sampleRelation Self 
--patientId ExampleImporta 
--patientName Example12 
--patientGender M 
--patientDateOfBirth 08/04/1969 
--patientConsanguinity Unknown

}

#Complete Command Line Request 

C:\Dev\geneyx.analysis.api\scripts>python ga_uploadSamples.py --snvVcf "C:\Users\eliws\OneDrive\Desktop\Geneyx\Production\scripts\GeneyxEval.vcf.gz" --sampleId Example3 --sampleSequenceDate 01/02/03 --sampleTakenDate 02/03/04 --sampleReceiveDate 03/18/22 --seqMachineId "NextSeq 2000" --kitId "Default - Exons only" --sampleType DnaSeq --sampleTarget Exome --sampleSource GermLine --genomeBuild hg19 --sampleNotes DemonstrationImport --sampleRelation Self --patientId ExampleImporta --patientName Example12 --patientGender M --patientDateOfBirth 08/04/1969 --patientConsanguinity Unknown

#Response 

Uploading sample(s)
<Response [200]>
b'{"Code":"success","Data":null,"Info":null,"MoreInfo":null,"NeedEval":false}'