from bulk_checksum.compare import compare_checksums, load_checksum_file
from pathlib import Path

def test_no_difference__when__checksums_are_same():
    checksum1 = {
        "123456": "filepath",
        "232345": "filepath2"
    }

    checksum2 = checksum1

    diff = compare_checksums(checksum1, checksum2)

    assert len(diff["only_in_source"]) == 0
    assert len(diff["only_in_destination"]) == 0

def test_reports_extra_source_hash__when__source_has_additional_hash():
    checksum1 = {
        "123456": "filepath",
        "232345": "filepath2",
        "456689": "filepath3"
    }

    checksum2 = {
        "123456": "filepath",
        "232345": "filepath2"
    }

    diff = compare_checksums(checksum1, checksum2)

    assert diff["only_in_source"] == {"456689": "filepath3"}
    assert len(diff["only_in_destination"]) == 0


def test_reports_extra_destination_hash__when__destination_has_additional_hash():
    checksum1 = {
        "123456": "filepath",
        "232345": "filepath2",
        "456689": "filepath3"
    }

    checksum2 = {
        "123456": "filepath",
        "232345": "filepath2"
    }

    diff = compare_checksums(checksum2, checksum1)

    assert len(diff["only_in_source"]) == 0
    assert diff["only_in_destination"] == {"456689": "filepath3"}


def test_compares_checksum_files__when__loading_and_comparing():
    path1 = Path(__file__).parent / "data/checksum_source.json"
    path2 = Path(__file__).parent / "data/checksum_destination.json"

    checksum1 = load_checksum_file(path1)
    checksum2 = load_checksum_file(path2)

    print(checksum1)

    print(checksum2)

    diff = compare_checksums(checksum1, checksum2)

    assert len(diff["only_in_source"]) == 0
    assert diff["only_in_destination"] == {"nas_checksums.txt": "d41d8cd98f00b204e9800998ecf8427e"}
    assert diff["mismatches"]["Jool Journey/vall-coords.txt"]
