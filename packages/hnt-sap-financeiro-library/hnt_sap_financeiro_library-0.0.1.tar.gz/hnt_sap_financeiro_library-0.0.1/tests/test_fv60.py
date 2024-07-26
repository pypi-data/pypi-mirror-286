# from hnt_sap_financeiro import sap_gui
# from hnt_sap_financeiro.hnt_sap_gui import SapGui


# from hnt_sap_financeiro.hnt_sap_gui import SapGui


# from hnt_sap_financeiro.hnt_sap_gui import SapGui


import json
from hnt_sap_financeiro.hnt_sap_gui import SapGui


def test_create():
    with open("./devdata/json/taxa_FIN-43388.json", "r", encoding="utf-8") as payload_json: taxa = json.load(payload_json)

    result = SapGui().run_FV60(taxa)
    assert result['error'] is None
