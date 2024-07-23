#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile

from neurostatx.io.download import get_home, download_data, save_files_dict


download_data(save_files_dict(), keys=["data.zip"])
tmp_dir = tempfile.TemporaryDirectory()


def test_help(script_runner):
    ret = script_runner.run(["ConfirmatoryFA", "-h"])

    assert ret.success


def test_execution_factor_analysis(script_runner):
    os.chdir(os.path.expanduser(tmp_dir.name))
    in_dataset = os.path.join(get_home(), "data/factor_data.xlsx")
    out_folder = os.path.join(get_home(), "data/factor_results/")

    ret = script_runner.run([
        "ConfirmatoryFA",
        "--in-dataset", in_dataset,
        "--out-folder", out_folder,
        "--desc-columns", 1,
        "--id-column", "subjectkey",
        "--model", "efa1 =~ v1 + v3 + v6 + v7",
        "--model", "efa2 =~ v2 + v4 + v5",
        "-f", "-v", "-s"]
    )

    assert ret.success
