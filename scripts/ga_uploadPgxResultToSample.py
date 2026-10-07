#!/usr/bin/env python3
"""Upload PGx diplotype results to an existing Geneyx sample.

Long-read pipelines (PacBio, ONT) call PGx diplotypes themselves. Where those
results did not reach Geneyx automatically, convert the caller's output to the
Geneyx PGx format and upload it here.

Either give a file the Geneyx PGx parser already produced:

    ga_uploadPgxResultToSample.py --sampleId S123 --pgxFile geneyx-pgx-results.json

or give the caller's own output and let this script convert it first, using the
GeneyxPgxParser library from PyPI - the same conversion Geneyx runs internally:

    ga_uploadPgxResultToSample.py --sampleId S123 --pharmcatFile HG002.pbstarphase.json

Run install.py once after cloning to get the libraries this needs.
"""

import argparse
import json
import ntpath
import os
import tempfile

import requests

import ga_helperFunctions as funcs


# ---------------------------------
# Define the command line parameters
# ---------------------------------
parser = argparse.ArgumentParser(
    prog="ga_uploadPgxResultToSample.py",
    description="Uploads PGx diplotype results to an existing sample",
)

# the file - either already converted, or the caller's own output
parser.add_argument("--pgxFile", help="The path to a Geneyx PGx results file (JSON)")
parser.add_argument(
    "--pharmcatFile",
    help="The path to a PharmCAT / pbStarPhase output file, converted "
    "to the Geneyx PGx format before it is uploaded",
)

# sample data
parser.add_argument("--sampleId", help="The sample id (serial number)", required=True)

# commands (optional)
parser.add_argument(
    "--config", "-c", help="configuration file", default="ga.config.yml"
)

args = parser.parse_args()

# read the config file
config = funcs.loadYamlFile(args.config)

# ---------------------------------
# Validation
# ---------------------------------
if args.pgxFile is None and args.pharmcatFile is None:
    raise Exception("Give either --pgxFile or --pharmcatFile")

if args.pgxFile is not None and args.pharmcatFile is not None:
    raise Exception("Give only one of --pgxFile or --pharmcatFile")

for path in (args.pgxFile, args.pharmcatFile):
    if path is not None and not os.path.exists(path):
        raise Exception("The file {} does not exist".format(path))


# ---------------------------------
# Conversion, when the caller's own output was given
# ---------------------------------
def convertToGeneyxPgx(callerFile, outputDir):
    """Convert a PharmCAT / pbStarPhase file with the Geneyx PGx parser library."""
    try:
        from GeneyxPgxParser import GeneyxPgxParser as PgxParser
    except ImportError:
        raise Exception(
            "The Geneyx PGx parser is not installed. Run: python3 install.py"
        )

    outputJson = "geneyx-pgx-results.json"
    request = {
        "output_json": outputJson,
        "input_dir": os.path.dirname(os.path.abspath(callerFile)),
        "output_dir": outputDir,
        "input_files": [ntpath.basename(callerFile)],
    }
    print(f"Converting {callerFile} to the Geneyx PGx format")
    PgxParser(request).run()

    converted = os.path.join(outputDir, outputJson)
    if not os.path.exists(converted):
        raise Exception(
            "The PGx parser produced no output for {}. Check that the file is a "
            "PharmCAT or pbStarPhase result.".format(callerFile)
        )
    return converted


# ---------------------------------
# File preparation
# ---------------------------------
workingDir = None
pgxFile = args.pgxFile
if pgxFile is None:
    workingDir = tempfile.mkdtemp()
    pgxFile = convertToGeneyxPgx(args.pharmcatFile, workingDir)

# Report what is about to be sent: the server rejects a file naming no gene it
# reports on, and seeing the gene list makes that answer obvious rather than
# surprising.
try:
    with open(pgxFile, "r") as handle:
        genes = [entry.get("Id") for entry in json.load(handle)]
    print(
        f"Uploading {len(genes)} gene(s): {', '.join(g for g in genes if g)}"
    )
except Exception as error:
    raise Exception(
        "{} is not a Geneyx PGx results file (expected a JSON array of gene "
        "results): {}".format(pgxFile, error)
    )

# ---------------------------------
# prepare the parameters for upload
# ---------------------------------
data = {
    "apiUserKey": config["apiUserKey"],
    "apiUserID": config["apiUserId"],
    "sampleSn": args.sampleId,
}

files = {"pgxResultFile": open(pgxFile, "rb")}
api = config["server"] + "/api/UploadPgxResultToSample"
print(f"Uploading PGx results to sample {args.sampleId}")
r = requests.post(api, data=data, files=files, timeout=60)
print(r)
print(r.content)
