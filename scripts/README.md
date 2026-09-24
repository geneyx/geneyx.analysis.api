# Geneyx API scripts

Python scripts for working with the Geneyx Analysis API. Full documentation is on the
[wiki](https://github.com/geneyx/geneyx.analysis.api/wiki).

## Setup

After cloning, run this once:

```bash
python3 install.py
```

It installs [requirements.txt](requirements.txt) and then checks that each Geneyx
library imports, because a successful `pip` run and a working install are not the same
thing.

```
--user      install into the user site-packages (no admin rights needed)
--upgrade   move to the newest allowed version of each package
```

Or install by hand:

```bash
pip install -r requirements.txt
```

Python 3.9+ is required.

## The Geneyx libraries

The scripts here use the same implementations the Geneyx pipeline runs, published on
PyPI, so a file you produce locally matches what Geneyx produces internally:

| Package                                                                            | Does                                                                      | Used by                         |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------- |
| [UnifyVcf](https://pypi.org/project/UnifyVcf/)                                     | Unifies SV / CNV / tandem-repeat / ROH calls into one structural VCF      | `UnifyVcf/*.py`                 |
| [pharmcatparser](https://pypi.org/project/pharmcatparser/)                         | Converts PharmCAT / pbStarPhase PGx output to the Geneyx PGx format       | `ga_uploadPgxResultToSample.py` |
| [AdvancedAnalysisFileParser](https://pypi.org/project/advancedanalysisfileparser/) | Parses secondary-pipeline TSV/JSON into the Geneyx advanced-analysis JSON | `AdvancedAnalysisFileParser/`   |

They ship as compiled wheels built per platform and Python version. If `pip` reports
_"No matching distribution found ... (from versions: none)"_, there is no build for your
Python version or platform — `install.py` says so explicitly. Tell Geneyx support which
you are on and we will add it.

## Configuration

Every `ga_*` script reads `ga.config.yml` (override with `--config`):

```yaml
server: "https://analysis.geneyx.com"
apiUserId: "enter-your-userid"
apiUserKey: "enter-your-userkey"
```

## Scripts

Each takes `--help`.

| Script                                           | Does                                                                       |
| ------------------------------------------------ | -------------------------------------------------------------------------- |
| `ga_createPatient.py`                            | Create a patient                                                           |
| `ga_CreateCase.py`                               | Create a case                                                              |
| `ga_uploadSample.py` / `ga_uploadSample_json.py` | Create a sample and upload its VCFs                                        |
| `ga_uploadFilesToSample.py`                      | Upload SNV/SV VCFs to an existing sample                                   |
| `ga_uploadBatch.py`                              | Upload a batch                                                             |
| `ga_addClinicalRecord.py`                        | Add a clinical record                                                      |
| `ga_addQcData.py`                                | Attach QC data to a sample                                                 |
| `ga_uploadPgxResultToSample.py`                  | Upload PGx diplotype results to a sample                                   |
| `UnifyVcf/`                                      | Unify structural VCFs before upload — see its [README](UnifyVcf/README.md) |
| `Misc/`, `RepModifyEpi2me/`                      | Format converters and one-off helpers                                      |

### Uploading PGx results

Long-read pipelines (PacBio, ONT) call PGx diplotypes themselves. Where those results
did not reach Geneyx automatically, upload them:

```bash
# the caller's own output, converted here before upload
python3 ga_uploadPgxResultToSample.py --sampleId S123 --pharmcatFile HG002.pbstarphase.json

# a file already in the Geneyx PGx format
python3 ga_uploadPgxResultToSample.py --sampleId S123 --pgxFile geneyx-pgx-results.json
```

The server validates the file before storing it: it must parse as a Geneyx PGx results
array, contain at least one gene, and contain at least one gene Geneyx reports on for
the sample's genome build. A sample whose PGx results came from a Geneyx pipeline run
cannot have them replaced by an upload — delete the existing PGx record first. Uploading
again replaces a previous upload.
