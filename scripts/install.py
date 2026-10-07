#!/usr/bin/env python3
"""Install everything the scripts in this folder need.

A git clone cannot carry installed packages, so this is the one step to run
after pulling:

    python3 install.py

It installs requirements.txt and then imports each Geneyx library, because a
successful pip run and a working install are not the same thing - the Geneyx
libraries ship as compiled wheels built per platform and Python version, so the
failure worth catching here is "no wheel for this interpreter", which pip
reports and people scroll past.

    --user      install into the user site-packages (no admin rights needed)
    --upgrade   move to the newest allowed version of each package
"""

import argparse
import subprocess
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_REQUIREMENTS = os.path.join(_HERE, "requirements.txt")

# Import name against the name people would look for; the two differ often
# enough that reporting the distribution name alone is not much help.
_GENEYX_LIBRARIES = [
    ("UnifyVcf", "UnifyVcf"),
    ("GeneyxPgxParser", "GeneyxPgxParser"),
    ("AdvancedAnalysisFileParser", "AdvancedAnalysisFileParser"),
]


def install(user=False, upgrade=False):
    command = [sys.executable, "-m", "pip", "install", "-r", _REQUIREMENTS]
    if user:
        command.append("--user")
    if upgrade:
        command.append("--upgrade")

    print("Running: " + " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")

    if result.returncode:
        _explainFailure((result.stdout or "") + (result.stderr or ""))
    return result.returncode


def _explainFailure(output):
    """Turn pip's "No matching distribution found" into something actionable.

    The Geneyx libraries are built per platform and Python version. On a Python
    they were not built for, pip reports "(from versions: none)" - which reads
    like the package does not exist, rather than like this interpreter is the
    problem.
    """
    if "No matching distribution found" not in output:
        return

    running = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(
        f"\nThis looks like there is no Geneyx build for Python {running} on "
        f"{sys.platform}.\n"
        "The Geneyx libraries ship as compiled wheels built per platform and "
        "Python version, so a version we have not built for finds nothing at all "
        "rather than falling back to source.\n\n"
        "Either use a Python we publish for, or tell Geneyx support you need "
        f"Python {running} on {sys.platform} and we will add it.")


def verify():
    """Import each Geneyx library and report the ones that did not resolve."""
    missing = []
    for module_name, distribution in _GENEYX_LIBRARIES:
        try:
            module = __import__(module_name)
        except Exception as error:
            missing.append((distribution, error))
            print(f"  FAILED   {distribution} (import {module_name}): {error}")
            continue
        version = getattr(module, "__version__", "")
        print(f"  ok       {distribution} {version}".rstrip())
    return missing


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="install.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--user",
        action="store_true",
        help="install into the user site-packages (no admin rights needed)",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="move to the newest allowed version of each package",
    )
    args = parser.parse_args(argv)

    if sys.version_info < (3, 9):
        print(
            f"Python {sys.version_info.major}.{sys.version_info.minor} is too old. "
            "The Geneyx libraries need Python 3.9 or newer."
        )
        return 1

    if not os.path.isfile(_REQUIREMENTS):
        print(f"requirements.txt not found beside this script ({_REQUIREMENTS})")
        return 1

    failed = install(user=args.user, upgrade=args.upgrade)
    if failed:
        print("\npip failed. Nothing was verified.")
        return failed

    print("\nChecking the Geneyx libraries import:")
    missing = verify()
    if missing:
        print(
            "\nSome libraries did not import. The usual cause is that no wheel is "
            f"published for Python {sys.version_info.major}.{sys.version_info.minor} "
            f"on this platform - the Geneyx libraries are built per platform and "
            "Python version. Tell Geneyx support which you are on and we will add it."
        )
        return 1

    print("\nDone. The scripts in this folder are ready to run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
