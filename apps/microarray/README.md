# Microarray file converter to VCF
For processing Microarray files in Geneyx it is required to convert those files to VCF files and then upload the VCF files to Geneyx.
The Microarray file converter does exactly that.
Its currently support the following Microarray file formats:
* Affymetrix

#Installation packages
There are two installation packages, for Window and for Linux

#Linux installation:
download and extract linux-x64.zip
install .net runtime version 8
sudo apt update && sudo apt install dotnet-runtime-8.0

give exe permission
sudo chmod 777  Tgex.Microarray.Converter

#Window installation:
download and extract win-x64.zip
install .net runtime version 8 for windows from https://dotnet.microsoft.com/en-us/download/dotnet/8.0


#Command example:
./Tgex.Microarray.Converter -i 1.txt -f Affymetrix -o 1.vcf