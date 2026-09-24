"""Guards the ONT append-chr script's call into the UnifyVcf package.

The script used to pass its skip-SVTYPE flag positionally, where UnifyVcf.run
receives roh_bed_path. Two things went wrong and neither was visible from the
call site: the flag never applied, and the unifier treated True as an ROH input,
reading file descriptor 1 and closing the process's own stdout. So what is pinned
here is the argument mapping itself, not only the resulting file - a fourth
positional argument would produce the same silence again.

The mapping tests are load-bearing for a reason worth knowing: **the output tests
cannot catch that bug.** Under a real console, reading fd 1 raises
``OSError: [Errno 9] Bad file descriptor``; under pytest's capture, fd 1 is a
readable temporary file, so the read succeeds, returns an empty buffer, and the
ROH input is quietly skipped as empty. The crash only reproduces with ``-s``.

Needs UnifyVcf >= 0.2.0, where repeat marking is decided per record.
"""

import gzip
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ONT_AppendChr

_META = "##fileformat=VCFv4.2\n"
_COLUMNS = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n"


def _record(chrom, pos, info="SVTYPE=DEL"):
    return f"{chrom}\t{pos}\t.\tN\t<DEL>\t.\tPASS\t{info}\tGT\t0/1\n"


def _write(directory, name, *records):
    path = directory / name
    path.write_text(_META + _COLUMNS + "".join(records), encoding="utf-8")
    return str(path)


def _read(unified_path):
    with gzip.open(unified_path, "rt", encoding="utf-8") as handler:
        return handler.read()


@pytest.fixture
def inputs(tmp_path):
    """An SV file with bare chromosome names and an ONT repeat file that has SVTYPE."""
    sv_path = _write(
        tmp_path, "sample.sv.vcf", _record("1", "100"), _record("chr2", "200")
    )
    repeat_path = _write(
        tmp_path, "sample.repeats.vcf", _record("1", "300", info="SVTYPE=STR;RU=CAG")
    )
    return sv_path, repeat_path, str(tmp_path / "unified.vcf")


# ---------------------------------------------------------------------------
# The argument mapping
# ---------------------------------------------------------------------------


def test_nothing_is_passed_as_the_roh_input(inputs, monkeypatch):
    # The regression itself: a flag in this slot both fails to apply and makes the
    # unifier read it as a file path.
    sv_path, repeat_path, output_path = inputs
    called = {}
    monkeypatch.setattr(
        ONT_AppendChr,
        "run",
        lambda *args, **kwargs: called.update(args=args, kwargs=kwargs),
    )

    ONT_AppendChr.main(["-o", output_path, "-s", sv_path, "-r", repeat_path])

    assert called["args"] == (), "every argument must be passed by keyword"
    assert "roh_bed_path" not in called["kwargs"]
    assert set(called["kwargs"]) == {
        "output_path",
        "sv_path",
        "cnv_path",
        "repeat_path",
    }


def test_the_paths_reach_the_arguments_they_belong_to(inputs, monkeypatch):
    sv_path, repeat_path, output_path = inputs
    called = {}
    monkeypatch.setattr(ONT_AppendChr, "run", lambda **kwargs: called.update(kwargs))

    ONT_AppendChr.main(["-o", output_path, "-s", sv_path, "-r", repeat_path])

    assert called["output_path"] == output_path
    assert called["sv_path"] == sv_path
    assert called["repeat_path"] == repeat_path
    assert called["cnv_path"] is None


# ---------------------------------------------------------------------------
# The file it produces
# ---------------------------------------------------------------------------


def test_it_unifies_without_an_roh_input(inputs):
    # This is what used to raise OSError: [Errno 9] Bad file descriptor.
    sv_path, repeat_path, output_path = inputs

    unified = ONT_AppendChr.main(["-o", output_path, "-s", sv_path, "-r", repeat_path])

    assert unified == output_path + ".gz"
    content = _read(unified)
    assert "<ROH>" not in content
    assert "SVTYPE=ROH" not in content


def test_ont_repeat_records_are_left_unmarked(inputs):
    # What the old skip_svtype flag was reaching for: a record already carrying
    # SVTYPE=STR must not be given a second type.
    sv_path, repeat_path, output_path = inputs

    content = _read(
        ONT_AppendChr.main(["-o", output_path, "-s", sv_path, "-r", repeat_path])
    )

    assert "SVTYPE=REP" not in content
    assert "SVTYPE=STR" in content


def test_a_repeat_record_with_no_type_of_its_own_is_marked(tmp_path):
    # The other half, and why the flag is gone rather than passed by keyword:
    # forcing skip-SVTYPE would send STRaglr calls to Geneyx unreadable as repeats.
    sv_path = _write(tmp_path, "sample.sv.vcf", _record("1", "100"))
    repeat_path = _write(
        tmp_path, "sample.repeats.vcf", _record("1", "300", info="RU=CAG")
    )
    output_path = str(tmp_path / "unified.vcf")

    content = _read(
        ONT_AppendChr.main(["-o", output_path, "-s", sv_path, "-r", repeat_path])
    )

    assert "RU=CAG;SVTYPE=REP" in content


def test_the_chr_prefix_is_added_to_records_and_not_to_headers(inputs):
    sv_path, repeat_path, output_path = inputs

    content = _read(
        ONT_AppendChr.main(["-o", output_path, "-s", sv_path, "-r", repeat_path])
    )

    assert content.startswith(_META)
    assert "\nchr1\t100\t" in content
    assert "\nchr2\t200\t" in content
    # Already prefixed, so not prefixed twice.
    assert "chrchr" not in content


def test_prefixing_the_same_file_twice_changes_nothing(inputs):
    # A failed run leaves the inputs rewritten, so the retry has to be safe.
    sv_path, _, _ = inputs

    ONT_AppendChr.add_chr_prefix_to_variants(sv_path)
    once = open(sv_path, encoding="utf-8").read()
    ONT_AppendChr.add_chr_prefix_to_variants(sv_path)

    assert open(sv_path, encoding="utf-8").read() == once
