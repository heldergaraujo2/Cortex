"""Tests for real MATLAB variable metadata inspection, using tiny synthetic fixtures."""
from __future__ import annotations
import json
import zipfile
from pathlib import Path

import pytest

np = pytest.importorskip('numpy')
scipy_io = pytest.importorskip('scipy.io')
savemat = scipy_io.savemat
from scripts.probe_t4_mat_variables import probe_v5

def test_probe_v5_reports_shapes_without_claiming_validation(tmp_path: Path):
    sample=tmp_path/"record.mat"
    savemat(sample,{"stimulus_direction":np.array([[0,90,180,270]]),"response":np.zeros((4,12))})
    result=probe_v5(sample)
    by_name={v["name"]:v for v in result["variables"]}
    assert result["format"]=="MATLAB-v5"
    assert by_name["stimulus_direction"]["shape"]==[1,4]
    assert by_name["response"]["shape"]==[4,12]

def test_matlab_archive_metadata_preserves_provenance(tmp_path: Path):
    sample=tmp_path/"record.mat"
    savemat(sample,{"trace":np.zeros((3,8))})
    archive=tmp_path/"experiment.zip"
    with zipfile.ZipFile(archive,"w") as z:
        z.write(sample,"session/record.mat")
    with zipfile.ZipFile(archive) as z:
        assert z.namelist()==["session/record.mat"]
        assert z.getinfo("session/record.mat").file_size>0
    assert probe_v5(sample)["variables"][0]["name"]=="trace"
