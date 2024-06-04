# GA-VCF Uploader
The VCF_Uploader contains features that enable batch upload of VCF files as well as upload of joint VCF files that contain multiple samples. To run this feature, download the zipped file and extract the contents. 
1. The first thing that you will need to do is modify the Tgex.VCFUploader.exe.config file with your account credentials (API ID and API Key). Please contact support@geneyx.com if you do not ahve this information. 
2. Next, navigate to the Resources folder. This folder contains an excel document that will need to be updated with the files that you want to import and placed in the directory where the VCF files are located. 
* For files that contian both SNV and CNV/SV, you only need to specify the sampleID once. If the SNV and CNV/SV VCF files have the same naming convention, the GA_VCF    uploader will recognize them automatically.  
3. Next, open Tgex.VCFUploader.exe. 
4. In the bottom left, click Select File, and select the updated excel file. 
5. Next, you can define a protocol, which will be applied to all samples, or you can leave the protocol blank. 
6. Select import. 
This will upload all samples into the given account. 