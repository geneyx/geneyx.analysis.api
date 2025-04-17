# Geneyx Sample Upload and Unification Workflow

This document provides an overview of the process for unifying multiple VCF files (CNV, SV, Repeat) and uploading samples in bulk to Geneyx using the provided scripts and configurations. It outlines the necessary steps to ensure that your data is correctly formatted and uploaded.

---

## 1. **Unification of VCF Files**

### Overview:
The unification process streamlines the consolidation of multiple VCF files related to **Copy Number Variations (CNV)**, **Structural Variations (SV)**, and **repeats**. The goal is to merge and adjust these files so that they meet Geneyx's requirements for sample uploads.

### Steps:
1. **Unify CNV, SV, TRGT/STR Files**: 
   - **UnifyVcf Script**: The `UnifyVcf` script is designed to combine the VCF files from different providers. Due to slight variations in file formats, this script adjusts the files to ensure they contain the necessary fields for Geneyx to read and process them correctly.
   - It’s essential to run the **UnifyVcf Script** that matches the pipeline used to create your original VCF files.
   
2. **Tutorial and Resources**:
   - A detailed video tutorial is available to guide you through the unification process. You can watch it [here](https://geneyx.com/?s=unification).
   - The script is hosted on GitHub and can be accessed at: [Geneyx UnifyVcf Scripts](https://github.com/geneyx/geneyx.analysis.api/tree/main/scripts/UnifyVcf).

### Important Notes:
- Ensure that you unify the **CNV**, **SV**, and **TRGT/STR** files using the unification script before proceeding with the upload.
  
---

## 2. **Batch Upload of Samples**

### Overview:
Once your VCF files are unified, the next step is to upload your samples in batch using the **JSON file** and associated **Python script**.

### Files:
- **BatchSampleJSON.json**: This file contains the sample information needed for the batch upload.
  - For a full list of API fields, refer to this [link](https://geneyx.com/?s=unification).
- **JSON_Sample_Upload.py**: The Python script that processes the **BatchSampleJSON.json** file and uploads the samples.

### Steps to Upload Samples:
1. **Ensure Files are in the Same Directory**:
   - Place the following files in the same directory as `JSON_Sample_Upload.py`:
     - `ga.config.yml`
     - `ga_helperFunctions.py`
   
2. **Run the Upload Command**:
   Open your terminal or command prompt and run the following command:
   
   ```bash```
   `python3 ga_uploadSample.py --jsonFile /path/to/your/sample_info.json --config /path/to/your/ga.config.yml`

## Configuration File

- **ga.config.yml**: This configuration file includes your Geneyx credentials and other setup details.

If you do not have access to the credentials, contact [support@geneyx.com](mailto:support@geneyx.com) or your local **Geneyx FAS** representative.

---

## 3. **Creating Cases in Geneyx**

### Overview:
Once the samples are uploaded, you can create cases manually in the Geneyx environment or use the **Batch Case Upload Script** to create cases in bulk.

### Steps:

#### **Manual Case Creation**:
- Cases can be manually created in the Geneyx interface once the samples are uploaded.

#### **Batch Case Upload Script**:
You can use the batch case upload script and the associated JSON file to automate case creation:

- [Batch Create Cases Script](https://github.com/geneyx/geneyx.analysis.api/blob/main/scripts/BatchCreateCases_json.py)
- [Batch Case JSON Template](https://github.com/geneyx/geneyx.analysis.api/blob/main/scripts/templates/BatchCaseList.json)

### Resources:
For further details, you can explore the full documentation and examples provided in the GitHub repository: [Geneyx Analysis API Scripts](https://github.com/geneyx/geneyx.analysis.api).

---

## Conclusion

By following these steps, you can successfully unify your CNV/SV/repeat VCF files, upload your samples in batch, and create cases within the Geneyx platform. If you have any issues or need assistance, please reach out to [support@geneyx.com](mailto:support@geneyx.com) or your local **Geneyx FAS** representative.

---

### **Additional Help & Support**:
For any troubleshooting or questions, feel free to contact [support@geneyx.com](mailto:support@geneyx.com).
