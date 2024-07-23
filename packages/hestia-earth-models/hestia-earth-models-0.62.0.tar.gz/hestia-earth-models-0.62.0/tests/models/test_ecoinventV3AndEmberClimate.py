import csv
from typing import Tuple, Dict, List
from unittest.mock import patch
import json
import pytest

from tests.utils import fixtures_path, fake_new_emission
from hestia_earth.models.ecoinventV3AndEmberClimate import MODEL, _should_run_emission, run

class_path = f"hestia_earth.models.{MODEL}"
fixtures_folder = f"{fixtures_path}/{MODEL}"

cycle_with_country = {"endDate": "2010", "site": {"country": {"@type": "Term", "termType": "region"}}}
cycle_without_country = {"endDate": "2010", "site": {"country": {}}}
ELECTRICITY_TERMS = [
    {"@type": "Term", "@id": "electricityGridMarketMix"},
    {"@type": "Term", "@id": "electricityGridRenewableMix"}
]


@pytest.mark.parametrize(
    "cycle,inputs,complete,expected_should_run",
    [
        (cycle_without_country, [], False, (False, [])),
        (
            cycle_without_country,
            [{"@type": "Input", "term": {"@id": "electricityGridMarketMix"}}],
            True,
            (False, [{"@type": "Input", "term": {"@id": "electricityGridMarketMix"}}])
        ),
        (cycle_with_country, [], True, (False, [])),
        (
            cycle_with_country,
            [{"@type": "Input", "term": {"@id": "electricityGridRenewableMix"}}],
            False,
            (False, [{"@type": "Input", "term": {"@id": "electricityGridRenewableMix"}}])
        ),
        (
            cycle_with_country,
            [{"@type": "Input", "term": {"@id": "electricityGridMarketMix"}}],
            True,
            (True, [{"@type": "Input", "term": {"@id": "electricityGridMarketMix"}}])
        ),
    ]
)
@patch(f"{class_path}.get_electricity_grid_mix_terms", return_value=ELECTRICITY_TERMS)
@patch(f"{class_path}._is_term_type_complete")
def test_should_run_emission(
    mock_complete, mock_get_terms, cycle: Dict, inputs: List, complete: bool, expected_should_run: Tuple
):
    mock_complete.return_value = complete
    cycle["inputs"] = inputs
    assert _should_run_emission(cycle, ELECTRICITY_TERMS, term_id="test") == expected_should_run


@patch(f"{class_path}.get_electricity_grid_mix_terms", return_value=ELECTRICITY_TERMS)
@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
@patch(f"{class_path}.utils.ecoinventV3_emissions")
def test_run(mock_ecoinventV3_emissions, *args):
    with open(f"{fixtures_path}/ecoinventV3_excerpt.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, quotechar='"')
        ecoinvent_fixture_rows = list(reader)

    test_terms = {
        "ch4ToAirInputsProductionFossil",      # 0.4
        "ch4ToAirInputsProductionNonFossil",   # 0.5
        "co2ToAirInputsProduction",            # 0.2
        "n2OToAirInputsProduction"             # 0.3
    }

    # Create a dictionary indexed by eco_invent_name
    # with list of tuples (emissions_term, value)
    mock_dict = dict()
    for row_dict in ecoinvent_fixture_rows:
        # create list of (emissions terms, values)
        terms_values_list = []
        for k in filter(lambda x: x.endswith(".term.@id"), row_dict.keys()):
            if row_dict[k] in test_terms:
                terms_values_list.append((row_dict[k], row_dict[f"emissionsResourceUse.{k.split('.')[1]}.value"]))

        mock_dict[row_dict["ecoinventName"]] = terms_values_list

    name = "electricity, high voltage, electricity production, wood, future"
    mock_ecoinventV3_emissions.return_value = mock_dict[name]

    with open(f"{fixtures_folder}/cycle.jsonld", encoding="utf-8") as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding="utf-8") as f:
        expected = json.load(f)

    value = run('all', cycle)
    assert value == expected
