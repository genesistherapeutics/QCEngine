"""
Tests the DQM compute dispatch module
"""

# Important this is first
from . import addons

import os
import qcengine as dc

@addons.using_psi4
def test_psi4():
    json_data = {}
    # json_data["molecule"] = """He 0 0 0\n--\nHe 0 0 1"""
    json_data["molecule"] = dc.get_molecule("water")
    json_data["driver"] = "energy"
    json_data["model"] = {"method": "SCF", "basis": "sto-3g"}
    json_data["keywords"] = {"scf_type": "df"}
    json_data["return_output"] = False

    ret = dc.compute(json_data, "psi4")

    assert ret["driver"] == "energy"
    for key in ["provenance", "wall_time"]:
        assert key in ret

    for key in ["cpu", "hostname", "username"]:
        assert key in ret["provenance"]

    assert ret["success"] == True

@addons.using_psi4
def test_psi4_ref_switch():
    json_data = {}
    json_data["molecule"] = dc.get_molecule("lithium")
    json_data["driver"] = "energy"
    json_data["model"] = {"method": "SCF", "basis": "sto-3g"}
    json_data["keywords"] = {"scf_type": "df"}
    json_data["return_output"] = False

    ret = dc.compute(json_data, "psi4")

    assert ret["success"] == True

@addons.using_rdkit
def test_rdkit():
    json_data = {}
    json_data["molecule"] = dc.get_molecule("water")
    json_data["molecule"]["connectivity"] = [[0, 1, 1], [0, 2, 1]]
    json_data["driver"] = "gradient"
    json_data["model"] = {"method": "UFF", "basis": ""}
    json_data["keywords"] = {}
    json_data["return_output"] = False

    ret = dc.compute(json_data, "rdkit")

    assert ret["success"] == True