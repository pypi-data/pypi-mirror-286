"""
ecoinvent v3 and Ember Climate

All emissions to air for the cycle.
"""
from functools import reduce
from typing import Tuple

from hestia_earth.utils.tools import list_sum, flatten
from hestia_earth.utils.model import linked_node
from hestia_earth.schema import EmissionMethodTier

from hestia_earth.models.log import logShouldRun, logRequirements, log_blank_nodes_id
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.blank_node import group_by_keys
from hestia_earth.models.utils.completeness import _is_term_type_complete
from hestia_earth.models.utils.term import get_electricity_grid_mix_terms
from hestia_earth.models.utils.cycle import cycle_end_year
from .utils import get_emission, get_all_emission_terms

REQUIREMENTS = {
    "Cycle": {
        "site": {
            "@type": "Site",
            "country": {"@type": "Term", "termType": "region"}
        },
        "inputs": [{
            "@type": "Input",
            "term.@id": ["electricityGridMarketMix", "electricityGridRenewableMix"],
            "value": ""
        }],
        "completeness.electricityFuel": "True"
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "background",
        "@type": "Emission",
        "inputs": ""
    }]
}
LOOKUPS = {
    "region-ember-energySources": "using `country`",
    "ember-ecoinvent-mapping": ["ember", "ecoinventId", "ecoinventName"]
}

MODEL = 'ecoinventV3AndEmberClimate'
MODEL_KEY = 'impactAssessment'  # keep to generate entry in "model-links.json"
TIER = EmissionMethodTier.BACKGROUND.value


def _emission(value: float, term_id: str, inputs: list, operation: dict) -> dict:
    emission = _new_emission(term_id, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['inputs'] = list(map(linked_node, inputs))
    if operation:
        emission["operation"] = operation
    return emission


def _grid_inputs(inputs: list, electricity_grid_terms: list):
    electricity_grid_term_ids = [v.get('@id') for v in electricity_grid_terms]
    return [
        i for i in inputs if i.get("term", {}).get("@id") in electricity_grid_term_ids
    ]


def _run_input(cycle: dict, inputs: list, emission_term_id: str, electricity_grid_term: dict):
    electricity_grid_inputs = [electricity_grid_term]
    inputs = _grid_inputs(inputs, electricity_grid_inputs)

    def run(grouped_inputs: list):
        input = grouped_inputs[0]
        term_id = input.get('term', {}).get('@id')
        input_value = list_sum(flatten(input.get('value', []) for input in grouped_inputs))
        country_id = cycle.get("site", {}).get("country", {}).get("@id")
        year = cycle_end_year(cycle)
        value = get_emission(
            term_id=emission_term_id,
            country=country_id,
            energy=input_value,
            year=year,
            model=MODEL
        )

        logRequirements(cycle, model=MODEL, term=term_id,
                        input_value=input_value,
                        emission_value=value)

        should_run = all([input_value > 0, value])
        logShouldRun(cycle, MODEL, term_id, should_run, methodTier=TIER)

        return _emission(value, emission_term_id, electricity_grid_inputs, input.get("operation"))

    return list(map(run, _group_by_operation(inputs).values() if inputs else []))


def _group_by_operation(inputs: list) -> dict:
    return reduce(group_by_keys(['operation']), inputs, {})


def _run_emission(cycle: dict, electricity_grid_terms: list, inputs: list, emission_term_id: str) -> list:
    return flatten([
        _run_input(
            cycle=cycle,
            inputs=inputs,
            emission_term_id=emission_term_id,
            electricity_grid_term=electricity_grid_term
        ) for electricity_grid_term in electricity_grid_terms
    ])


def _should_run_emission(cycle: dict, electricity_grid_terms: list, term_id: str) -> Tuple[bool, list]:
    term_type_complete = _is_term_type_complete(cycle, 'electricityFuel')
    inputs = _grid_inputs(cycle.get('inputs', []), electricity_grid_terms)
    has_relevant_inputs = bool(inputs)
    has_country = bool(cycle.get("site", {}).get("country", {}))
    has_end_date = bool(cycle.get("endDate"))

    logRequirements(cycle, model=MODEL, term=term_id,
                    term_type_electricityFuel_complete=term_type_complete,
                    input_ids=log_blank_nodes_id(inputs),
                    has_relevant_inputs=has_relevant_inputs,
                    has_country=has_country,
                    has_end_date=has_end_date)

    should_run = all([term_type_complete, has_relevant_inputs, has_country, has_end_date])
    logShouldRun(cycle, MODEL, term_id, should_run, methodTier=TIER)
    return should_run, inputs


def _run_emissions(cycle: dict, electricity_grid_terms: list):
    def run_emissions_for_term(term_id: str) -> list:
        should_run, inputs = _should_run_emission(cycle, electricity_grid_terms, term_id)
        return _run_emission(cycle, electricity_grid_terms, inputs, term_id) if should_run else []
    return run_emissions_for_term


def run(_, cycle: dict):
    electricity_grid_terms = get_electricity_grid_mix_terms()
    return flatten(list(map(_run_emissions(cycle, electricity_grid_terms), get_all_emission_terms())))
