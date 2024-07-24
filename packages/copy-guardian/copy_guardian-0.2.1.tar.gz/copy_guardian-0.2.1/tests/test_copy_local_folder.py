import os

import pytest

from copy_guardian import copy_local_folder


def test_local_folder_copy(tmp_path_factory):
    in_folder = tmp_path_factory.mktemp("in")
    out_folder = tmp_path_factory.mktemp("out")

    (in_folder / "test.txt").write_text("abc")

    with pytest.raises(IOError):
        copy_local_folder(in_folder / "noexit", out_folder)

    with pytest.raises(IOError):
        copy_local_folder(in_folder / "test.txt", out_folder)

    with pytest.raises(IOError):
        copy_local_folder(in_folder, out_folder / "nonexist")

    copy_local_folder(in_folder, out_folder)
    assert [xi for x in list(os.walk(out_folder)) for xi in x[2]] == ["test.txt"]

    for base, sub_folder, files in os.walk(out_folder):
        if files == ["test.txt"]:
            with open(os.path.join(base, "test.txt")) as fh:
                assert fh.read() == "abc"
